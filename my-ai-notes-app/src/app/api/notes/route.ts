import { NextRequest, NextResponse } from 'next/server';


export async function POST(req: NextRequest) {
  console.log("process.env.NEXT_PUBLIC_API_BASE_URL", process.env.NEXT_PUBLIC_API_BASE_URL);
  try {
    const body = await req.json();
    const backendRes = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/notes/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const contentType = backendRes.headers.get("content-type");
    if (contentType?.includes("application/json")) {
      const data = await backendRes.json();
      return NextResponse.json(data, { status: backendRes.status });
    } else {
      const text = await backendRes.text();
      return new NextResponse(text, {
        status: backendRes.status,
        headers: { "Content-Type": "text/plain" }
      });
    }
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Proxy failed', details: String(error) }, { status: 500 });
  }
}
