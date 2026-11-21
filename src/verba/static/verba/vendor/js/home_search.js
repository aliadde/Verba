
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("note-search");
    const noteCards = document.querySelectorAll(".note-card");
    const resultsCount = document.getElementById("search-results-count");
    const emptyState = document.getElementById("search-empty-state");

    if (!searchInput) return;

    function renderSnippet(element, text, query, context = 40) {
        const lowerText = text.toLowerCase();
        const matches = [];
        let position = 0;

        // Find all matches
        while (position < text.length) {
            const index = lowerText.indexOf(query, position);
            if (index === -1) break;

            matches.push(index);
            position = index + query.length;
        }

        // Limit displayed matches
        const ranges = matches.slice(0, 3).map(index => ({
            start: Math.max(0, index - context),
            end: Math.min(text.length, index + query.length + context)
        }));

        // Merge overlapping ranges
        const merged = [];

        ranges.forEach(range => {
            const last = merged[merged.length - 1];

            if (last && range.start <= last.end) {
                last.end = Math.max(last.end, range.end);
            } else {
                merged.push({ ...range });
            }
        });

        const fragment = document.createDocumentFragment();

        merged.forEach((range, rangeIndex) => {
            if (rangeIndex > 0) fragment.append(" ... ");
            if (range.start > 0) fragment.append("...");

            let cursor = range.start;

            matches.forEach(index => {
                if (index < range.start || index >= range.end) return;

                fragment.append(
                    document.createTextNode(text.slice(cursor, index))
                );

                const mark = document.createElement("mark");
                mark.textContent = text.slice(index, index + query.length);
                fragment.append(mark);

                cursor = index + query.length;
            });

            fragment.append(
                document.createTextNode(text.slice(cursor, range.end))
            );

            if (range.end < text.length) fragment.append("...");
        });

        element.replaceChildren(fragment);
    }

    let searchTimeout;

    searchInput.addEventListener("input", () => {
        clearTimeout(searchTimeout);

        searchTimeout = setTimeout(() => {
            const query = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            noteCards.forEach(card => {
                const first = card.dataset.first || "";
                const second = card.dataset.second || "";

                const firstElement = card.querySelector(".note-preview-first");
                const secondElement = card.querySelector(".note-preview-second");

                if (!query) {
                    card.classList.remove("d-none");

                    firstElement.textContent = first.slice(0, 100);
                    secondElement.textContent = second.slice(0, 100);

                    visibleCount++;
                    return;
                }

                const firstMatch = first.toLowerCase().includes(query);
                const secondMatch = second.toLowerCase().includes(query);

                const matches = firstMatch || secondMatch;

                card.classList.toggle("d-none", !matches);

                if (!matches) return;

                visibleCount++;

                if (firstMatch) {
                    renderSnippet(firstElement, first, query);
                } else {
                    firstElement.textContent = first.slice(0, 100);
                }

                if (secondMatch) {
                    renderSnippet(secondElement, second, query);
                } else {
                    secondElement.textContent = second.slice(0, 100);
                }
            });

            // Update results count
            if (resultsCount) {
                resultsCount.textContent = query
                    ? `${visibleCount} of ${noteCards.length} notes found`
                    : `${noteCards.length} notes`;
            }

            // Show empty state
            if (emptyState) {
                emptyState.classList.toggle(
                    "d-none",
                    visibleCount !== 0 || !query
                );
            }

        }, 300);
    });

    // Initialize results count
    searchInput.dispatchEvent(new Event("input"));
});
