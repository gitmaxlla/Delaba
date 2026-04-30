import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("http://127.0.0.1:8000/v1/external/ai/health", () => {
    // Would be cool if json(false) 200 also counted as error cause it should
    return new HttpResponse(null, { status: 500 });
  }),

  http.post("http://127.0.0.1:8000/v1/external/ai", () => {
    console.log(123);
    return HttpResponse.json({ content: "AI Response" });
  }),
];
