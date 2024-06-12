interface IMessageSource {
  lessonName: string;
  subjectName: string;
  url: string;
  video: string;
  start: string;
  end: string;
}

interface IMessage {
  message: string;
  sources: IMessageSource[];
  error?: boolean;
}

interface IChat {
  messages: IMessage[];
  loading: boolean;
}
