import React, { Suspense } from "react";
import ProjectItem from "@/components/project/project-item";
import { ProjectRequest, ProjectType } from "@/types/projectType";
import { getProjects } from "@/api/project/getProjects";
import PaginationBar from "@/components/common/pagination";
import Link from "next/link";

export const dynamic = "force-dynamic";

const ProjectList = async ({
  searchParams,
}: {
  searchParams: ProjectRequest;
}) => {
  const response = await getProjects(searchParams);

  if (!response.data || !!response.error) {
    return (
      <div className="w-full flex flex-col items-center flex-grow mt-5">
        프로젝트를 불러오는 중 오류가 발생했습니다.
        {response.error && <p>{response.error || "알수없는 에러"}</p>}
      </div>
    );
  } else if (!response.data.data || response.data.data.length === 0) {
    return (
      <div className="w-full flex flex-col items-center flex-grow mt-5">
        <p className="text-[24px]">프로젝트가 없습니다</p>
        <p>
          <Link className="text-emerald-500 font-bold" href={"/project/create"}>
            여기
          </Link>
          를 눌러 프로젝트를 생성해 주세요.
        </p>
      </div>
    );
  }

  const projects: ProjectType[] = response.data.data;
  const totalPage = response.data.total_pages;
  const currentPage = response.data.page;
  const queryStrings = new URLSearchParams();
  if (searchParams.model_name) {
    queryStrings.set("model_name", searchParams.model_name);
  }
  if (searchParams.page) {
    queryStrings.set("page", searchParams.page);
  }
  return (
    <div className="w-full flex flex-col gap-1 items-center ">
      {projects.length > 0 ? (
        <div className="w-full flex flex-col items-center flex-grow mt-5 ">
          {projects.map((project) => (
            <ProjectItem key={project.project_id} project={project} />
          ))}
        </div>
      ) : (
        <div className="w-full flex flex-col items-center">
          <p>프로젝트가 없습니다.</p>
          <p>새로 생성해 주세요</p>
        </div>
      )}
      <PaginationBar
        queryStrings={queryStrings}
        totalPage={totalPage}
        currentPage={currentPage}
      />
    </div>
  );
};

interface PageProps {
  searchParams: {
    page?: string;
    model_name?: string;
  };
}

const Page = ({ searchParams }: PageProps) => {
  const nowPage = searchParams.page ? searchParams.page : "1";
  const searchRequest = {
    page: nowPage,
    limit: "10",
    ...(searchParams.model_name && { model_name: searchParams.model_name }),
  };
  return (
    <div className="bg-gray-100 dark:bg-gray-800 py-2 px-2 my-3 rounded-md w-full h-full flex flex-col items-center flex-grow remove_scrollbar">
      <Suspense
        key={`${searchParams.page || "1"}-${searchParams.model_name || ""}`}
        fallback={<div>Loading...</div>}
      >
        <ProjectList searchParams={searchRequest} />
      </Suspense>
    </div>
  );
};

export default Page;
