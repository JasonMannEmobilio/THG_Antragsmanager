import httpx
import asyncio

async def test_patch():
    url = "http://localhost:8090/records"
    data = {"id": 1, "status": "test_patch_script"}
    try:
        async with httpx.AsyncClient() as client:
            print(f"Sending PATCH to {url} with {data}")
            response = await client.patch(url, json=data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_patch())
