from uuid import UUID
from python_slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundError, AuthorizationError
from src.dao.agent import agent_dao
from src.schemas.agent import AgentCreate, AgentUpdate, AgentResponse


class AgentService:
    async def create_agent(
        self, session: AsyncSession, user_id: UUID, data: AgentCreate
    ) -> AgentResponse:
        agent_data = data.model_dump()
        agent_data["owner_id"] = user_id
        agent_data["slug"] = slugify(data.name)
        agent = await agent_dao.create(session, agent_data)
        return AgentResponse.model_validate(agent)

    async def get_agent(self, session: AsyncSession, agent_id: UUID) -> AgentResponse:
        agent = await agent_dao.get_by_id(session, agent_id)
        if not agent:
            raise NotFoundError("Agent", str(agent_id))
        return AgentResponse.model_validate(agent)

    async def update_agent(
        self, session: AsyncSession, agent_id: UUID, user_id: UUID, data: AgentUpdate
    ) -> AgentResponse:
        agent = await agent_dao.get_by_id(session, agent_id)
        if not agent:
            raise NotFoundError("Agent", str(agent_id))
        if str(agent.owner_id) != str(user_id):
            raise AuthorizationError("You don't own this agent")
        update_data = data.model_dump(exclude_unset=True)
        agent = await agent_dao.update(session, agent_id, update_data)
        return AgentResponse.model_validate(agent)

    async def delete_agent(self, session: AsyncSession, agent_id: UUID, user_id: UUID):
        agent = await agent_dao.get_by_id(session, agent_id)
        if not agent:
            raise NotFoundError("Agent", str(agent_id))
        if str(agent.owner_id) != str(user_id):
            raise AuthorizationError("You don't own this agent")
        await agent_dao.soft_delete(session, agent_id)

    async def list_user_agents(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        agents, total = await agent_dao.get_user_agents(session, user_id, page, page_size)
        return {
            "agents": [AgentResponse.model_validate(a) for a in agents],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def list_public_agents(self, session: AsyncSession, page: int = 1, page_size: int = 20):
        agents, total = await agent_dao.get_public_agents(session, page, page_size)
        return {
            "agents": [AgentResponse.model_validate(a) for a in agents],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def clone_agent(
        self, session: AsyncSession, agent_id: UUID, user_id: UUID
    ) -> AgentResponse:
        original = await agent_dao.get_by_id(session, agent_id)
        if not original:
            raise NotFoundError("Agent", str(agent_id))
        clone_data = {
            "name": f"{original.name} (Clone)",
            "slug": slugify(f"{original.name}-clone"),
            "description": original.description,
            "agent_type": original.agent_type,
            "system_prompt": original.system_prompt,
            "model": original.model,
            "provider": original.provider,
            "temperature": original.temperature,
            "max_tokens": original.max_tokens,
            "tools": original.tools,
            "is_public": False,
            "category": original.category,
            "tags": original.tags,
            "config": original.config,
            "owner_id": user_id,
        }
        agent = await agent_dao.create(session, clone_data)
        return AgentResponse.model_validate(agent)


agent_service = AgentService()
