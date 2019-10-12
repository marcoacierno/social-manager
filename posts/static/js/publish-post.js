(function() {
    let activeTab = null;
    let movingLamp = null;
    let previews = {};

    function onPageLoaded(e) {
        const tabs = document.querySelector(".publish-post--tabs");

        movingLamp = tabs.querySelector(".publish-post--tabs--lamp");
        // previews = {
        //     'facebook': document.querySelector('.publish-post--preview #preview--facebook'),
        // }

        [...tabs.querySelectorAll("li")].forEach(tab => {
            if (tab.classList.contains("active")) {
                activeTab = tab;
            }

            tab.addEventListener("click", onTabChange.bind(null, tab));
        });
    }

    function onTabChange(tab, e) {
        activeTab.classList.remove("active");
        activeTab = tab;

        const index = parseInt(tab.getAttribute("data-index"), 10);
        movingLamp.style.transform = `translateX(${100 * index}%)`;

        activeTab.classList.add("active");

        showPreview(activeTab.getAttribute("data-preview-type"));
    }

    function showPreview(type) {}

    window.addEventListener("load", onPageLoaded);
})();
