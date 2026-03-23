import { useState, useCallback, useEffect } from "react";
import "./App.css";
import type { Feed, Article } from "./types";
import { fetchFeeds, fetchArticles, createFeed, deleteFeed } from "./api";
import { useWebSocket, type FeedStatus } from "./useWebsocket";

const STATUS_LABEL: Record<FeedStatus["status"], string> = {
  fetching: "⏳ Downloading...",
  summarizing: "🤖 Summarizing",
  done: "Done",
};

function App() {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [newFeedTitle, setNewFeedTitle] = useState("");
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedFeedId, setSelectedFeedId] = useState<number | null>(null);
  const [newFeedUrl, setNewFeedUrl] = useState("");
  const [feedStatuses, setFeedStatuses] = useState<Record<number, FeedStatus>>(
    () => {
      const saved = sessionStorage.getItem("feedStatuses");
      return saved ? JSON.parse(saved) : {};
    },
  );

  useEffect(() => {
    fetchFeeds().then(setFeeds);
  }, []);

  useEffect(() => {
    fetchArticles(selectedFeedId ?? undefined).then(setArticles);
  }, [selectedFeedId]);

  useEffect(() => {
    sessionStorage.setItem("feedStatuses", JSON.stringify(feedStatuses));
  }, [feedStatuses]);

  const handleArticle = useCallback((article: Article) => {
    setArticles((prev) => {
      if (prev.some((a) => a.id === article.id)) return prev;
      return [article, ...prev];
    });
  }, []);

  const handleStatus = useCallback(
    (feed_id: number, statusInfo: FeedStatus) => {
      if (statusInfo.status === "done") {
        setFeedStatuses((prev) => {
          const next = { ...prev };
          delete next[feed_id];
          return next;
        });
      } else {
        setFeedStatuses((prev) => ({ ...prev, [feed_id]: statusInfo }));
      }
    },
    [],
  );

  useWebSocket({ onArticle: handleArticle, onStatus: handleStatus });

  const handleAddFeed = async () => {
    if (!newFeedUrl.trim()) return;
    const created = await createFeed(
      newFeedUrl.trim(),
      newFeedTitle.trim() || undefined,
    );
    setFeeds((prev) => [...prev, created]);
    setNewFeedUrl("");
    setNewFeedTitle("");
    setFeedStatuses((prev) => ({
      ...prev,
      [created.id]: { status: "fetching" },
    }));
  };

  const handleDeleteFeed = async (id: number) => {
    await deleteFeed(id);
    setFeeds((prev) => prev.filter((f) => f.id !== id));
    if (selectedFeedId === id) setSelectedFeedId(null);
  };

  return (
    <div className="mx-auto max-w-6xl p-4 grid grid-cols-[300px_1fr] gap-4 h-screen">
      <aside className="flex flex-col gap-3 bg-gray-50 border border-gray-200 rounded-xl p-4 overflow-y-auto">
        <h2 className="text-lg font-semibold text-gray-800">Feeds</h2>

        <div className="flex flex-col gap-2">
          <input
            type="text"
            value={newFeedTitle}
            onChange={(e) => setNewFeedTitle(e.target.value)}
            placeholder="Title (optional)"
            className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div className="flex gap-2">
            <input
              type="url"
              value={newFeedUrl}
              onChange={(e) => setNewFeedUrl(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAddFeed()}
              placeholder="https://example.com/feed.xml"
              className="flex-1 text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleAddFeed}
              className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3 py-2 rounded-lg transition-colors"
            >
              Add
            </button>
          </div>
        </div>
        <ul className="flex flex-col gap-1">
          {feeds.length === 0 && (
            <li className="text-sm text-gray-400 text-center py-4">
              No feeds yet
            </li>
          )}
          {feeds.map((feed) => {
            const statusInfo = feedStatuses[feed.id];
            return (
              <li
                key={feed.id}
                onClick={() =>
                  setSelectedFeedId(selectedFeedId === feed.id ? null : feed.id)
                }
                className={`flex flex-col gap-1 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                  selectedFeedId === feed.id
                    ? "bg-blue-100 text-blue-800 font-medium"
                    : "hover:bg-gray-100 text-gray-700"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm truncate">
                    {feed.title ?? feed.url}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteFeed(feed.id);
                    }}
                    className="text-red-400 hover:text-red-600 text-xs px-2 py-0.5 rounded hover:bg-red-50 transition-colors shrink-0"
                  >
                    Delete
                  </button>
                </div>
                {statusInfo && (
                  <span className="text-xs text-gray-500">
                    {STATUS_LABEL[statusInfo.status]}
                    {statusInfo.status === "summarizing" &&
                      statusInfo.title && (
                        <span className="ml-1 block text-gray-400">
                          {statusInfo.title}
                        </span>
                      )}
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      </aside>

      <main className="flex flex-col gap-3 overflow-y-auto border border-gray-200 rounded-xl p-4 border-shadow-sm">
        <h2 className="text-lg font-semibold text-gray-800">
          {selectedFeedId
            ? (feeds.find((f) => f.id === selectedFeedId)?.title ?? "Articles")
            : "All Articles"}
        </h2>

        {articles.length === 0 ? (
          <p className="text-sm text-gray-400 text-center py-10">
            No articles found
          </p>
        ) : (
          <ul className="flex flex-col gap-3">
            {articles.map((article) => (
              <li
                key={article.id}
                className="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-sm transition-shadow"
              >
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline font-medium text-base"
                >
                  {article.title}
                </a>
                {article.summary && (
                  <p
                    title={article.summary}
                    className="text-sm text-gray-600 mt-1 line-clamp-3"
                  >
                    {article.summary}
                  </p>
                )}
                {article.published_at && (
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(article.published_at).toLocaleDateString(
                      "pl-PL",
                      {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      },
                    )}
                  </p>
                )}
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}

export default App;
