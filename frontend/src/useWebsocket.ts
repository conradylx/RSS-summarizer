import { useEffect, useRef } from "react";
import type { Article } from "./types";

type FeedStatus = {
  status: "fetching" | "summarizing";
  title?: string;
};

type WSMessage =
  | ({ type: "article" } & Article)
  | ({ type: "status"; feed_id: number } & FeedStatus);

type UseWebSocketProps = {
  onArticle: (article: Article) => void;
  onStatus: (feed_id: number, status: FeedStatus) => void;
};

export function useWebSocket({ onArticle, onStatus }: UseWebSocketProps) {
  const wsRef = useRef<WebSocket | null>(null);
  const onArticleRef = useRef(onArticle);
  const onStatusRef = useRef(onStatus);

  useEffect(() => {
    onArticleRef.current = onArticle;
    onStatusRef.current = onStatus;
  }, [onArticle, onStatus]);

  useEffect(() => {
    function connect() {
      const ws = new WebSocket("ws://localhost:8000/ws/");

      ws.onmessage = (event) => {
        const data: WSMessage = JSON.parse(event.data);
        if (data.type === "article") {
          onArticleRef.current(data);
        } else if (data.type === "status") {
          onStatusRef.current(data.feed_id, {
            status: data.status,
            title: data.title,
          });
        }
      };

      ws.onclose = () => {
        setTimeout(connect, 3000);
      };

      wsRef.current = ws;
    }

    connect();

    return () => {
      wsRef.current?.close();
    };
  }, []);
}

export type { FeedStatus };
