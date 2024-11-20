"use client";

import { customFetch } from "@/app/actions/customFetch";
import { DefaultPaginationType, PaginationType } from "@/types/default";
import { ProjectType } from "@/types/projectType";
import { Pagination, Spinner } from "@nextui-org/react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import ProjectItem from "./project-item";

const ProjectList = () => {
  const queryclient = useQueryClient();
  const searchParams = useSearchParams();
  const [page, setPage] = useState<number>(
    parseInt(searchParams.get("page") || "1")
  );
  const [model_name, setModelName] = useState<string | null>(
    searchParams.get("model_name")
  );

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
    queryclient.invalidateQueries({
      queryKey: ["projects"],
    });
  };

  const searchParams_Input = new URLSearchParams({
    page: page.toString(),
  });
  if (model_name) searchParams_Input.set("model_name", model_name);

  const { data, isPending, isLoading, isError, error } = useQuery<
    PaginationType<ProjectType[]>,
    string,
    PaginationType<ProjectType[]>,
    [string]
  >({
    staleTime: 1000 * 60 * 10,
    gcTime: 1000 * 60 * 60,
    queryKey: ["projects"],
    queryFn: async () => {
      const response = await customFetch<DefaultPaginationType<ProjectType[]>>({
        endpoint: `/project/list`,
        method: "GET",
        searchParams: searchParams_Input,
      });

      if (!response.data) {
        throw new Error("No data received from server");
      }
      if (response.error) {
        throw new Error(`Server error: ${response.error}`);
      }
      if (!response.data.data) {
        throw new Error("Invalid data structure received");
      }

      return response.data.data;
    },
  });

  if (isPending || isLoading)
    return (
      <div>
        <Spinner size="lg" />
      </div>
    );
  if (isError) return <div>Error loading projects</div>;
  if (!data || !data.data) return <div>No projects found</div>;

  return (
    <div className="w-full h-full flex flex-col items-center justify-between  pb-2">
      <div className="w-full overflow-y-auto flex flex-col items-center justify-center">
        {data.data.map((project) => (
          <ProjectItem key={project.project_id} project={project} />
        ))}
      </div>
      <div className="flex flex-col mt-2">
        <Pagination
          showControls
          size="lg"
          onChange={handlePageChange}
          total={data.total_pages}
          initialPage={page}
        />
      </div>
    </div>
  );
};

export default ProjectList;
