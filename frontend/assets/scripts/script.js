function highlightActiveNav() {
  const path = window.location.pathname;
  // console.log('====================================');
  // console.log(path);
  // console.log('====================================');
  const pages = [
    { page: "index.html", id: "nav-home" },
    { page: "activities.html", id: "nav-activities" },
    { page: "push.html", id: "nav-push" },
    { page: "pushrequest.html", id: "nav-pull" },
    { page: "merge.html", id: "nav-merge" }
  ];

  pages.forEach(({ page, id }) => {
    const link = document.getElementById(id);
    if (!link) return;

    if (path.includes(page)) {
      link.classList.remove("text-gray-900");
      link.classList.add("text-blue-700", "font-semibold");
    }
  });
}

highlightActiveNav();
