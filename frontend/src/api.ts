import type { Article, Feed } from "./types";

const API_URL = "http://localhost:8000/api";

async function fetchFeeds(): Promise<Feed[]> {
  const response = await fetch(`${API_URL}/feeds/`);
  if (!response.ok) {
    throw new Error(`Failed to fetch feeds: ${response.statusText}`);
  }
  return response.json();
}

async function createFeed(url: string, title?: string): Promise<Feed> {
  const response = await fetch(`${API_URL}/feeds/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, title }),
  });
  if (!response.ok) {
    throw new Error(`Failed to create feed: ${response.statusText}`);
  }
  return response.json();
}

async function deleteFeed(id: number) {
  const response = await fetch(`${API_URL}/feeds/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error(`Failed to delete feed: ${response.statusText}`);
  }
  if (response.status !== 204) {
    return response.json();
  }
}

async function fetchArticles(feedId?: number): Promise<Article[]> {
  const url = feedId
    ? `${API_URL}/articles/?feed_id=${feedId}`
    : `${API_URL}/articles/`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch articles: ${response.statusText}`);
  }
  return response.json();
}

export { fetchFeeds, createFeed, deleteFeed, fetchArticles };
