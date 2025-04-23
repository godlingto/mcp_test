import asyncio  # asyncio 추가
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

server_params = StdioServerParameters(
    command="python",
    args=["/Users/junyoung-park/Lecture/AI Project Master/Projects/mcp_test/math_server.py"],  # 경로 수정 완료
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            result = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            print(result)  # 결과 출력

if __name__ == "__main__":
    try:
        asyncio.run(main())  # 일반 환경에서 실행
    except RuntimeError:  # 이미 이벤트 루프가 실행 중인 경우
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
