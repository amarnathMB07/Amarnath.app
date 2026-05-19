import mongoose from "mongoose";

const MessageSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "Please provide a name."],
      trim: true,
      maxlength: [60, "Name cannot be more than 60 characters"],
    },
    email: {
      type: String,
      required: [true, "Please provide an email."],
      match: [
        /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        "Please fill a valid email address",
      ],
    },
    message: {
      type: String,
      required: [true, "Please provide a message."],
      maxlength: [1000, "Message cannot be more than 1000 characters"],
    },
  },
  { timestamps: true }
);

export default mongoose.models.Message || mongoose.model("Message", MessageSchema);
