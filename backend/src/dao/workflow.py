from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.workflow import Workflow, WorkflowExecution


class WorkflowDAO(BaseDAO[Workflow]):
    def __init__(self):
        super().__init__(Workflow)

    async def get_user_workflows(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        return await self.get_all(session, page, page_size, filters={"owner_id": user_id})

    async def get_public_workflows(self, session: AsyncSession, page: int = 1, page_size: int = 20):
        return await self.get_all(session, page, page_size, filters={"is_public": True})


class WorkflowExecutionDAO(BaseDAO[WorkflowExecution]):
    def __init__(self):
        super().__init__(WorkflowExecution)

    async def get_workflow_executions(
        self, session: AsyncSession, workflow_id: UUID, page: int = 1, page_size: int = 20
    ):
        return await self.get_all(session, page, page_size, filters={"workflow_id": workflow_id})


workflow_dao = WorkflowDAO()
workflow_execution_dao = WorkflowExecutionDAO()
