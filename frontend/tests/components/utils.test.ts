import { expect, test } from "vitest";
import { sortByDeadline } from "~/util";
import type { Task } from "~/types";

const tasks = [
  {
    channel: "",
    createdAt: "",
    deadline: "2026-05-10",
    fileHash: "",
    id: 0,
    modifiedAt: "",
    subject: "",
    title: "",
    type: "",
    subtasks: [],
  },

  {
    channel: "",
    createdAt: "",
    deadline: "2026-10-05",
    fileHash: "",
    id: 0,
    modifiedAt: "",
    subject: "",
    title: "",
    type: "",
    subtasks: [],
  },
];

test("dates are sorted from earliest to oldest", () => {
  expect(sortByDeadline(tasks)).not.toEqual(tasks);
});
