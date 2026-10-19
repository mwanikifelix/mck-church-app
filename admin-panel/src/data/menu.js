/*
 * Main navigation for the MCK Wesley admin panel.
 *
 * 'to' points at the route NAME (not the path), as required by BaseNavigation.
 * Nodes with a 'heading' render as a section label in the sidebar.
 */

export default {
  main: [
    // --- Overview ---
    { heading: true, name: "Overview" },
    { name: "Dashboard", to: "dashboard", icon: "fa fa-home" },

    // --- Community ---
    { heading: true, name: "Community" },
    { name: "Members", to: "members", icon: "fa fa-users" },
    { name: "Branches", to: "branches", icon: "fa fa-map-marker-alt" },
    { name: "Departments", to: "departments", icon: "fa fa-building" },
    { name: "Growth-Track Groups", to: "groups", icon: "fa fa-project-diagram" },
    { name: "HBC Groups", to: "hbc", icon: "fa fa-sitemap" },

    // --- Engagement ---
    { heading: true, name: "Engagement" },
    { name: "Events", to: "events", icon: "fa fa-calendar-alt" },
    { name: "Announcements", to: "announcements", icon: "fa fa-bullhorn" },
    { name: "Pastoral Care", to: "pastoral-care", icon: "fa fa-hands-helping" },
    { name: "Giving", to: "giving", icon: "fa fa-hand-holding-heart" },

    // --- Content ---
    { heading: true, name: "Content" },
    { name: "Content Library", to: "content-library", icon: "fa fa-book-open" },
    { name: "About Page Content", to: "about-content", icon: "fa fa-info-circle" },
    {
      name: "Registration Windows",
      to: "registration-windows",
      icon: "fa fa-door-open",
    },

    // --- Administration ---
    { heading: true, name: "Administration" },
    { name: "Roles & Permissions", to: "roles", icon: "fa fa-user-shield" },
  ],
};
