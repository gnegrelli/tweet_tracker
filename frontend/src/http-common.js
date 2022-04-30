import axios from "axios";

export default axios.create({
    baseURL: process.env.NEXT_PUBLIC_PROD ? "" : "http://localhost:8000",
    headers: {
        "Content-type": "application/json"
    }
});