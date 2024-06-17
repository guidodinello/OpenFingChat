import API from "@/services/api";

class ChatAPI {
  send(
    query: IQuery
  ): Promise<{ ok: boolean; data: IMessage; conversationId?: string }> {
    return API.post("/query", {
      query: query.query,
      conversation_id: query.conversationId || "",
    })
      .then((response) => ({
        ok: true,
        conversationId: response.data.conversation_id,
        data: {
          message: response.data.llm_response,
          sources: response.data.sources.map((s: any) => ({
            lessonName: s.lesson_name,
            subjectName: s.subject_name,
            url: s.url,
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
