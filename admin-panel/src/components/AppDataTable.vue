<script setup>
import { computed, ref, watch } from "vue";

/**
 * Bootstrap data table that replaces PrimeVue's <DataTable>/<Column> pair.
 *
 * Columns are declared as data rather than as nested components:
 *
 *   const columns = [
 *     { field: "full_name", header: "Name", sortable: true },
 *     { field: "status",    header: "Status", slot: "status" },
 *     // Dropped below xl so the primary columns never get clipped:
 *     { field: "membership_number", header: "Membership No.", below: "xl" },
 *   ]
 *
 *   <AppDataTable :rows="members" :columns="columns" :loading="loading">
 *     <template #status="{ row }"> ...badge... </template>
 *     <template #toolbar>
 *       <button class="btn btn-primary btn-sm">New Member</button>
 *     </template>
 *   </AppDataTable>
 *
 * Slot naming: a column with `slot: "status"` renders the template named
 * `status`. Columns without a `slot` render the `cell` template (or their
 * raw value). `toolbar` is reserved for the buttons above the table and is
 * deliberately separate from any per-row column slot — they must not share
 * a name, or the toolbar would invoke a row template with no row.
 *
 * Responsive behaviour:
 *  - >=768px: normal table inside a horizontally scrollable wrapper
 *  - <768px:  rows collapse into stacked cards with per-field labels
 */
const props = defineProps({
  rows: { type: Array, default: () => [] },
  columns: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  // null = show everything
  pageSize: { type: Number, default: 15 },
  searchable: { type: Boolean, default: true },
  searchPlaceholder: { type: String, default: "Search…" },
  exportName: { type: String, default: "" },
  emptyText: { type: String, default: "No records found." },
  emptyIcon: { type: String, default: "fa-inbox" },
  // Fields to search when a column has no `field`
  searchFields: { type: Array, default: null },
  initialSort: { type: Object, default: null }, // { field, dir: 'asc'|'desc' }
});

const emit = defineEmits(["row-click", "page-change"]);

const search = ref("");
const sortField = ref(props.initialSort?.field || "");
const sortDir = ref(props.initialSort?.dir || "asc");
const page = ref(1);

// --- search ---------------------------------------------------------------
const searchTarget = computed(() =>
  props.searchFields && props.searchFields.length
    ? props.searchFields
    : props.columns.map((c) => c.field).filter(Boolean)
);

function cellValue(row, col) {
  if (col.sortValue) return col.sortValue(row);
  return col.field ? row[col.field] : "";
}

function haystack(row) {
  return searchTarget.value
    .map((f) => {
      const v = typeof f === "function" ? f(row) : row[f];
      return v == null ? "" : String(v);
    })
    .join(" ")
    .toLowerCase();
}

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return props.rows;
  return props.rows.filter((r) => haystack(r).includes(q));
});

// --- sort -----------------------------------------------------------------
const sorted = computed(() => {
  if (!sortField.value) return filtered.value;
  const col = props.columns.find((c) => c.field === sortField.value);
  if (!col) return filtered.value;

  const dir = sortDir.value === "desc" ? -1 : 1;
  return [...filtered.value].sort((a, b) => {
    const av = cellValue(a, col);
    const bv = cellValue(b, col);
    if (av == null && bv == null) return 0;
    if (av == null) return 1;
    if (bv == null) return -1;
    if (typeof av === "number" && typeof bv === "number") return (av - bv) * dir;
    return String(av).localeCompare(String(bv), undefined, { numeric: true }) * dir;
  });
});

// --- pagination -----------------------------------------------------------
const pageCount = computed(() =>
  props.pageSize ? Math.max(1, Math.ceil(sorted.value.length / props.pageSize)) : 1
);

const paged = computed(() => {
  if (!props.pageSize) return sorted.value;
  const start = (page.value - 1) * props.pageSize;
  return sorted.value.slice(start, start + props.pageSize);
});

// Reset to page 1 whenever the result set shrinks below the current page
watch(pageCount, (n) => {
  if (page.value > n) {
    page.value = n;
    emit("page-change", page.value);
  }
});

watch(search, () => {
  if (page.value !== 1) page.value = 1;
});

function toggleSort(col) {
  if (!col.sortable) return;
  if (sortField.value === col.field) {
    sortDir.value = sortDir.value === "asc" ? "desc" : "asc";
  } else {
    sortField.value = col.field;
    sortDir.value = "asc";
  }
}

function sortIcon(col) {
  if (!col.sortable) return "fa-sort";
  if (sortField.value !== col.field) return "fa-sort";
  return sortDir.value === "asc" ? "fa-sort-up" : "fa-sort-down";
}

/**
 * Responsive column priority. Declaring `below: "xl"` on a column keeps it
 * visible from Bootstrap's xl breakpoint up, and drops it entirely below that
 * — both as a table cell and as a row in the stacked mobile layout. Use it for
 * secondary fields (membership numbers, timestamps) so the primary columns
 * never get clipped or squeezed on narrower screens.
 */
const RESPONSIVE_STEPS = ["sm", "md", "lg", "xl", "xxl"];
function hideBelow(col) {
  if (!col.below || !RESPONSIVE_STEPS.includes(col.below)) return null;
  return `d-none d-${col.below}-table-cell`;
}

function goTo(p) {
  page.value = Math.min(Math.max(1, p), pageCount.value);
  emit("page-change", page.value);
}

// --- export ---------------------------------------------------------------
function exportCsv() {
  if (!props.rows.length) return;
  const cols = props.columns.filter((c) => c.field && c.header);
  const esc = (v) => {
    const s = v == null ? "" : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = [
    cols.map((c) => esc(c.header)).join(","),
    ...sorted.value.map((r) => cols.map((c) => esc(cellValue(r, c))).join(",")),
  ];
  const blob = new Blob(["\uFEFF" + lines.join("\n")], {
    type: "text/csv;charset=utf-8;",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${props.exportName || "export"}-${new Date()
    .toISOString()
    .slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

const rangeStart = computed(() =>
  sorted.value.length ? (page.value - 1) * (props.pageSize || sorted.value.length) + 1 : 0
);
const rangeEnd = computed(() =>
  Math.min(page.value * (props.pageSize || sorted.value.length), sorted.value.length)
);
</script>

<template>
  <div class="app-table">
    <!-- Toolbar -->
    <div
      v-if="searchable || exportName || $slots.actions"
      class="d-flex flex-column flex-sm-row gap-2 align-items-stretch align-items-sm-center justify-content-between mb-3"
    >
      <div class="d-flex gap-2 align-items-center flex-grow-1">
        <div v-if="searchable" class="input-group input-group-sm" style="max-width: 22rem">
          <span class="input-group-text">
            <i class="fa fa-search opacity-50"></i>
          </span>
          <input
            v-model="search"
            type="search"
            class="form-control"
            :placeholder="searchPlaceholder"
            :aria-label="searchPlaceholder"
          />
        </div>
        <span v-if="search" class="fs-sm text-muted d-none d-sm-inline">
          {{ filtered.length }} of {{ rows.length }}
        </span>
      </div>

      <div class="d-flex gap-2 align-items-center">
        <slot name="toolbar"></slot>
        <button
          v-if="exportName && rows.length"
          type="button"
          class="btn btn-sm btn-alt-secondary"
          :aria-label="`Export ${rows.length} records to CSV`"
          @click="exportCsv"
        >
          <i class="fa fa-download me-1"></i>
          Export CSV
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="table-responsive">
      <table class="table table-striped table-hover align-middle mb-0 app-table-el">
        <thead>
          <tr>
            <th
              v-for="col in columns"
              :key="col.field || col.header"
              :class="[
                {
                  'cursor-pointer': col.sortable,
                  'text-end': col.align === 'end',
                  'text-center': col.align === 'center',
                },
                hideBelow(col),
              ]"
              :style="col.width ? { width: col.width } : null"
              scope="col"
              @click="toggleSort(col)"
            >
              {{ col.header }}
              <i v-if="col.sortable" class="fa ms-1 opacity-50 fs-xs" :class="sortIcon(col)"></i>
            </th>
          </tr>
        </thead>

        <tbody>
          <!-- Loading skeleton -->
          <template v-if="loading">
            <tr v-for="n in pageSize || 5" :key="`sk-${n}`">
              <td v-for="c in columns" :key="c.header" class="ps-0">
                <span class="placeholder-glow w-100">
                  <span class="placeholder rounded" style="height: 1rem"></span>
                </span>
              </td>
            </tr>
          </template>

          <!-- Empty state -->
          <template v-else-if="!paged.length">
            <tr>
              <td :colspan="columns.length" class="text-center py-5">
                <i class="fa fa-2x opacity-25 mb-2 d-block" :class="emptyIcon"></i>
                <p class="text-muted mb-0">{{ search ? "No matches for “" + search + "”." : emptyText }}</p>
              </td>
            </tr>
          </template>

          <!-- Rows -->
          <tr
            v-for="(row, i) in paged"
            v-else
            :key="row.id ?? i"
            class="app-table-row"
            @click="$emit('row-click', row)"
          >
            <td
              v-for="col in columns"
              :key="col.field || col.header"
              :data-label="col.header"
              :class="[
                {
                  'text-end': col.align === 'end',
                  'text-center': col.align === 'center',
                  'fw-semibold': col.strong,
                },
                hideBelow(col),
              ]"
            >
              <slot :name="col.slot || 'cell'" :row="row" :value="cellValue(row, col)" :column="col">
                {{ cellValue(row, col) ?? "—" }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Footer: count + pager -->
    <div
      v-if="!loading && rows.length"
      class="d-flex flex-column flex-sm-row gap-2 align-items-sm-center justify-content-between mt-3"
    >
      <div class="fs-sm text-muted">
        Showing <strong>{{ rangeStart }}</strong>–<strong>{{ rangeEnd }}</strong>
        of <strong>{{ sorted.length }}</strong>
        <span v-if="search"> matching “{{ search }}”</span>
      </div>

      <nav v-if="pageCount > 1" aria-label="Table pagination">
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item" :class="{ disabled: page === 1 }">
            <button class="page-link" type="button" aria-label="Previous" @click="goTo(page - 1)">
              <i class="fa fa-chevron-left"></i>
            </button>
          </li>
          <li
            v-for="p in pageCount"
            :key="p"
            class="page-item"
            :class="{ active: p === page }"
          >
            <button class="page-link" type="button" @click="goTo(p)">{{ p }}</button>
          </li>
          <li class="page-item" :class="{ disabled: page === pageCount }">
            <button class="page-link" type="button" aria-label="Next" @click="goTo(page + 1)">
              <i class="fa fa-chevron-right"></i>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
  user-select: none;
}
.app-table-el thead th {
  white-space: nowrap;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--bs-body-color);
  opacity: 0.7;
  border-bottom-width: 1px;
  background-color: var(--bs-body-bg);
}

/*
 * Below 768px the table stops being a table and becomes a stack of cards,
 * with each cell labelled from its column header. This is what keeps wide
 * tables (members, permissions) usable on a phone.
 */
@media (max-width: 767.98px) {
  .app-table-el,
  .app-table-el tbody,
  .app-table-el tr,
  .app-table-el td {
    display: block;
    width: 100%;
  }
  .app-table-el thead {
    display: none;
  }
  .app-table-el tbody tr {
    border: 1px solid var(--bs-border-color);
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    padding: 0.5rem 0.75rem;
    background-color: var(--bs-body-bg);
  }
  .app-table-el td {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    text-align: right !important;
    border: none;
    padding: 0.35rem 0;
    border-bottom: 1px dashed var(--bs-border-color);
  }
  .app-table-el td:last-child {
    border-bottom: none;
  }
  .app-table-el td::before {
    content: attr(data-label);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    opacity: 0.6;
    text-align: left;
    flex-shrink: 0;
  }
  .app-table-el td > * {
    margin-left: auto;
  }
}
</style>
