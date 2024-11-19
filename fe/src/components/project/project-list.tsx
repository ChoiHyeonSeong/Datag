import { PaginationType } from "@/types/default";
import { ProjectType } from "@/types/projectType";
import ProjectItem from "./project-item";
import PaginationBar from "../common/pagination";
import React from "react";

const ProjectList = ({
  data,
  queryStrings,
}: {
  data: PaginationType<ProjectType[]>;
  queryStrings: URLSearchParams;
}) => {
  const projects = data.data;
  return (
    <div className="w-full flex flex-col gap-1 items-center">
      <div className="w-full flex flex-col items-center flex-grow mt-5">
        {projects.map((project) => (
          <ProjectItem key={project.project_id} project={project} />
        ))}
      </div>
      <PaginationBar
        queryStrings={queryStrings}
        totalPage={data.total_pages}
        currentPage={data.page}
      />
    </div>
  );
};

export default ProjectList;
