import { NextResponse } from "next/server";
import connectDB from "@/lib/mongodb";
import Message from "@/models/Message";

export async function POST(request) {
  try {
    const { name, email, message } = await request.json();

    if (!name || !email || !message) {
      return NextResponse.json(
        { error: "Name, email, and message are required." },
        { status: 400 }
      );
    }

    const db = await connectDB();
    
    if (db) {
       // Save to DB if connection is successful
       const newMessage = await Message.create({ name, email, message });
       console.log("Message saved to database:", newMessage);
    } else {
       // Mock success if no DB configured (for easy demo/deployment without DB)
       console.log("Mock message received:", { name, email, message });
    }

    return NextResponse.json(
      { message: "Message sent successfully!" },
      { status: 201 }
    );
  } catch (error) {
    console.error("Error saving message:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
