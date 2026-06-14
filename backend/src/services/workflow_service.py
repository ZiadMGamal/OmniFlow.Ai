from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundError, AuthorizationError
from src.dao.workflow import workflow_dao, workflow_execution_dao
from src.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowExecuteRequest,
    WorkflowExecutionResponse,
)


class WorkflowService:
    async def create_workflow(
        self, session: AsyncSession, user_id: UUID, data: WorkflowCreate
    ) -> WorkflowResponse:
        wf_data = data.model_dump()
        wf_data["owner_id"] = user_id
        workflow = await workflow_dao.create(session, wf_data)
        return WorkflowResponse.model_validate(workflow)

    async def get_workflow(self, session: AsyncSession, workflow_id: UUID) -> WorkflowResponse:
        workflow = await workflow_dao.get_by_id(session, workflow_id)
        if not workflow:
            raise NotFoundError("Workflow", str(workflow_id))
        return WorkflowResponse.model_validate(workflow)

    async def update_workflow(
        self, session: AsyncSession, workflow_id: UUID, user_id: UUID, data: WorkflowUpdate
    ) -> WorkflowResponse:
        workflow = await workflow_dao.get_by_id(session, workflow_id)
        if not workflow:
            raise NotFoundError("Workflow", str(workflow_id))
        if str(workflow.owner_id) != str(user_id):
            raise AuthorizationError("You don't own this workflow")
        update_data = data.model_dump(exclude_unset=True)
        workflow = await workflow_dao.update(session, workflow_id, update_data)
        return WorkflowResponse.model_validate(workflow)

    async def delete_workflow(self, session: AsyncSession, workflow_id: UUID, user_id: UUID):
        workflow = await workflow_dao.get_by_id(session, workflow_id)
        if not workflow:
            raise NotFoundError("Workflow", str(workflow_id))
        if str(workflow.owner_id) != str(user_id):
            raise AuthorizationError("You don't own this workflow")
        await workflow_dao.soft_delete(session, workflow_id)

    async def list_user_workflows(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        workflows, total = await workflow_dao.get_user_workflows(session, user_id, page, page_size)
        return {
            "workflows": [WorkflowResponse.model_validate(w) for w in workflows],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def execute_workflow(
        self, session: AsyncSession, workflow_id: UUID, data: WorkflowExecuteRequest
    ) -> WorkflowExecutionResponse:
        workflow = await workflow_dao.get_by_id(session, workflow_id)
        if not workflow:
            raise NotFoundError("Workflow", str(workflow_id))

        execution = await workflow_execution_dao.create(session, {
            "workflow_id": workflow_id,
            "status": "running",
            "trigger_type": data.trigger_type,
            "input_data": data.input_data,
            "node_results": [],
        })

        try:
            results = await self._run_workflow_nodes(workflow, data.input_data)
            await workflow_execution_dao.update(session, execution.id, {
                "status": "completed",
                "output_data": results.get("output", {}),
                "node_results": results.get("node_results", []),
                "duration_ms": results.get("duration_ms", 0),
            })
        except Exception as e:
            await workflow_execution_dao.update(session, execution.id, {
                "status": "failed",
                "error": str(e),
            })

        execution = await workflow_execution_dao.get_by_id(session, execution.id)
        return WorkflowExecutionResponse.model_validate(execution)

    async def _run_workflow_nodes(self, workflow, input_data: dict) -> dict:
        node_results = []
        current_data = input_data

        for node in workflow.nodes:
            node_result = {
                "node_id": node.get("id"),
                "type": node.get("type"),
                "status": "completed",
                "output": current_data,
            }
            node_results.append(node_result)

        return {
            "output": current_data,
            "node_results": node_results,
            "duration_ms": 0,
        }

    async def get_executions(
        self, session: AsyncSession, workflow_id: UUID, page: int = 1, page_size: int = 20
    ):
        executions, total = await workflow_execution_dao.get_workflow_executions(
            session, workflow_id, page, page_size
        )
        return {
            "executions": [WorkflowExecutionResponse.model_validate(e) for e in executions],
            "total": total,
            "page": page,
            "page_size": page_size,
        }


workflow_service = WorkflowService()
