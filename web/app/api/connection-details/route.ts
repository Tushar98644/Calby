import { NextResponse } from 'next/server';
import axios from 'axios';

const FASTAPI_URL = process.env.FASTAPI_BACKEND_URL;

export const revalidate = 0;

export type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

export async function POST(req: Request) {
  try {
    if (process.env.LIVEKIT_URL === undefined) {
      throw new Error('LIVEKIT_URL is not defined');
    }
    if (FASTAPI_URL === undefined) {
      throw new Error('FASTAPI_BACKEND_URL is not defined');
    }
    
    const participantName = 'user';
    const participantIdentity = `voice_assistant_user_${Math.floor(Math.random() * 10_000)}`;
    const roomName = `voice_assistant_room_${Math.floor(Math.random() * 10_000)}`;

    const backendUrl = `${FASTAPI_URL}/api/v1/get-livekit-token?room_name=${roomName}&identity=${participantIdentity}`;
    console.log(`Fetching token from: ${backendUrl}`);
    
    const backendResponse = await axios.get(backendUrl);
    if (backendResponse.status !== 200) {
      throw new Error(`Failed to get token from backend: ${backendResponse.statusText}`);
    }

    const backendData = backendResponse.data;
    const participantToken = backendData.token;

    const data: ConnectionDetails = {
      serverUrl: process.env.LIVEKIT_URL,
      roomName,
      participantToken: participantToken,
      participantName,
    };

    const headers = new Headers({
      'Cache-Control': 'no-store',
    });
    return NextResponse.json(data, { headers });

  } catch (error) {
    if (error instanceof Error) {
      console.error(error);
      return new NextResponse(error.message, { status: 500 });
    }
  }
}