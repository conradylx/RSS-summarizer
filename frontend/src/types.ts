export type Feed = {
  id: number;
  url: string;
  title: string;
  created_at: string;
};

export type Article = {
  id: number;
  title: string;
  url: string;
  summary: string | null;
  published_at: string | null;
};
