from skeleton_cli.agents.base import Agent
from skeleton_cli.config.settings import Settings
from skeleton_cli.core.ports import LanguageModel
from skeleton_cli.providers.registry import create_provider


def build_model(settings: Settings) -> LanguageModel:
    return create_provider(settings.provider, model=settings.model)


def build_agent(settings: Settings) -> Agent:
    return Agent(
        name="default-agent",
        system_prompt=settings.system_prompt,
        model=build_model(settings),
    )
