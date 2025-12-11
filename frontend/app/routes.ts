import { type RouteConfig, route, index } from "@react-router/dev/routes";

export default [
    index("routes/index.tsx"),
    route("/home", "routes/home.tsx"),
    route("/subject/:name/:focusId?", "routes/subject.tsx"),
    route("/settings", "routes/settings.tsx"),
    
    // route("/plan", "routes/plan.tsx"),
    // route("/news", "routes/news.tsx"),
    // route("/card", "routes/card.tsx"),
] satisfies RouteConfig;