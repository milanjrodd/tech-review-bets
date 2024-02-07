import type { APIRoute } from "astro";

const getProxyUrl = (request: Request) => {
  const proxyUrl = new URL("http://0.0.0.0:8000");
  const requestUrl = new URL(request.url);

  return new URL(requestUrl.pathname, proxyUrl);
};

export const ALL: APIRoute = async ({ request }) => {
  const proxyUrl = getProxyUrl(request);
  const response = await fetch(proxyUrl.href, request);
  return new Response(response.body);
};
