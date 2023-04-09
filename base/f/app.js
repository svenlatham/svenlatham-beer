/* Sven's app */


(function() {

    var app = (function() {
        var elResults = document.getElementById("results");
        function init() {
            load();
        }

        async function load() {
            const response = await fetch("metadata.json");
            const jsonData = await response.json();
            processData(jsonData);
        }

        function createDom(item) {
            var dom = document.createElement("DIV");
            var domRow = document.createElement("DIV");
            var domImageColumn = document.createElement("DIV");
            var domTextColumn = document.createElement("DIV");
            var domCardBody = document.createElement("DIV");
            domCardBody.classList.add("card-body");

            var h1 = document.createElement("H5");
            h1.classList.add("card-title");
            h1.appendChild(document.createTextNode(item.name));
            var description = document.createElement("P");
            description.appendChild(document.createTextNode(item.description));
            dom.classList.add("card");
            dom.classList.add("mb-3");
            dom.style.width = "540px";
            domRow.classList.add("row");
            domRow.classList.add("g-0");
            domImageColumn.classList.add("col-3");

            if (item.image) {
                var domImg = document.createElement("IMG");
                domImg.setAttribute("src", item.image);
                domImageColumn.appendChild(domImg);
            }

            domTextColumn.classList.add("col-9");




            domCardBody.appendChild(h1);
            domCardBody.appendChild(description);
            domTextColumn.appendChild(domCardBody);

            domRow.appendChild(domImageColumn);
            domRow.appendChild(domTextColumn);
            dom.appendChild(domRow);
            return dom;
        }

        function processData(data) {
            var results = document.getElementById("results");
            results.innerHTML = ''; // Cheating
            for (var i in data) {
                // Create an element to handle this
                var dom = createDom(data[i]);
                results.appendChild(dom);

            }


        }



        return { init: init }
    })();

    app.init();



})()