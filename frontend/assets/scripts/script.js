function highlightActiveNav() {
  const path = window.location.pathname;

  const pages = [
    { page: "/frontend/index.html", id: "nav-home" },
    { page: "/frontend/activities.html", id: "nav-activities" },
    { page: "/frontend/push.html", id: "nav-push" },
    { page: "/frontend/pushrequest.html", id: "nav-pull" },
    { page: "/frontend/merge.html", id: "nav-merge" }
  ];

  pages.forEach(({ page, id }) => {
    const link = document.getElementById(id);
    if (!link) return;

    if (path.includes(page)) {
      link.classList.remove("text-gray-900");
      link.className = "text-blue-700"
      // link.classList.add("text-blue-700", "font-semibold");
    }
  });
}

highlightActiveNav();
