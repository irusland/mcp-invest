from mcp.server.fastmcp import FastMCP
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from tinkoff.invest import Client, GetAccountsResponse
from tinkoff.invest.services import Services


class InvestSettings(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(
        env_prefix="INVEST_",
        env_file="/Users/ruslansirazhetdinov/local-projects/mcp-invest/.env",
        env_nested_delimiter="__",
        nested_model_default_partial_update=True,
        extra="ignore",
    )


settings = InvestSettings()

class MCPInvestTools:
    def __init__(self, service: Services, mcp: FastMCP):
        self._service = service
        self._mcp = mcp
        mcp.add_tool(service.users.get_accounts)
        mcp.add_tool(service.instruments.find_instrument)
        mcp.add_tool(service.market_data.get_candles)


mcp = FastMCP("Invest")

with Client(settings.token.get_secret_value()) as service:
    invest_server = MCPInvestTools(service=service, mcp=mcp)
    mcp.run()
