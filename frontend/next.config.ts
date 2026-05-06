import type { NextConfig } from "next";

const isGitHubPages = process.env.GITHUB_PAGES === "true";
const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1] ?? "ticket";
const githubPagesBasePath = `/${repositoryName}`;

const nextConfig: NextConfig = {
  output: isGitHubPages ? "export" : "standalone",
  trailingSlash: isGitHubPages,
  basePath: isGitHubPages ? githubPagesBasePath : undefined,
  assetPrefix: isGitHubPages ? `${githubPagesBasePath}/` : undefined,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
