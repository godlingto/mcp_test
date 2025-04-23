import asyncio  # asyncio 추가
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

async def main():
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["/Users/junyoung-park/Lecture/AI Project Master/Projects/mcp_test/math_server.py"],  # 경로 수정 완료
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        math_res = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        print("Math Result:", math_res)  # 결과 출력
        weather_res = await agent.ainvoke({"messages": "what is the weather in nyc?"})
        print("Weather Result:", weather_res)  # 결과 출력

if __name__ == "__main__":
    try:
        asyncio.run(main())  # 일반 환경에서 실행
    except RuntimeError:  # 이미 이벤트 루프가 실행 중인 경우
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
