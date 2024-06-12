import API from "@/services/api";

class ChatAPI {
  send(query: IQuery): Promise<{ ok: boolean; data: IMessage }> {
    return API.post("/query", { query: query.query })
      .then((response) => ({
        ok: true,
        data: {
          message: response.data.llm_response,
          sources: response.data.sources.map((s: any) => ({
            lessonName: s.lesson_name,
            subjectName: s.subject_name,
            url: s.url,
            video: s.video,
            start: s.timestamps[0],
            end: s.timestamps[1],
          })),
        },
      }))
      .catch((err) => ({
        ok: false,
        data: { error: true, message: err.message, sources: [] },
      }));
  }
}

export default new ChatAPI();
