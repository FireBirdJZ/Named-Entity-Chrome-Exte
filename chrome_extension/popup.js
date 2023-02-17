// For Sending A post request to flask server to highlight entites on webpage
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("send-html").addEventListener("click", function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", tabs[0].url, true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var html = xhr.responseText;
          var xhr2 = new XMLHttpRequest();
          xhr2.open("POST", "http://127.0.0.1:5000/html", true);
          xhr2.setRequestHeader("Content-Type", "text/plain");
          xhr2.onreadystatechange = function() {
            if (xhr2.readyState == 4 && xhr2.status == 200) {
              var modifiedHtml = xhr2.responseText;
              chrome.tabs.executeScript(tabs[0].id, {
                code: "document.body.innerHTML = `" + modifiedHtml + "`;"
              });
            }
          };
          xhr2.send(html);
        }
      };
      xhr.send();
    });
  });
});

// New approach
// document.addEventListener("DOMContentLoaded", function() {
//   document.getElementById("send-html").addEventListener("click", function() {
//     chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//       var xhr = new XMLHttpRequest();
//       xhr.open("GET", tabs[0].url, true);
//       xhr.onreadystatechange = function() {
//         if (xhr.readyState == 4 && xhr.status == 200) {
//           var html = xhr.responseText;
//           var xhr2 = new XMLHttpRequest();
//           xhr2.open("POST", "http://127.0.0.1:5000/html", true);
//           xhr2.setRequestHeader("Content-Type", "text/plain");
//           xhr2.onreadystatechange = function() {
//             if (xhr2.readyState == 4 && xhr2.status == 200) {
//               var modifiedHtml = xhr2.responseText;
//               var div = document.createElement("div");
//               div.innerHTML = modifiedHtml;
//               document.body.appendChild(div);
//             }
//           };
//           xhr2.send(html);
//         }
//       };
//       xhr.send();
//     });
//   });
// });

// document.addEventListener("DOMContentLoaded", function() {
//   document.getElementById("send-html").addEventListener("click", function() {
//     chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//       var xhr = new XMLHttpRequest();
//       xhr.open("GET", tabs[0].url, true);
//       xhr.onreadystatechange = function() {
//         if (xhr.readyState == 4 && xhr.status == 200) {
//           var html = xhr.responseText;
//           var xhr2 = new XMLHttpRequest();
//           xhr2.open("POST", "http://127.0.0.1:5000/html", true);
//           xhr2.setRequestHeader("Content-Type", "text/plain");
//           xhr2.onreadystatechange = function() {
//             if (xhr2.readyState == 4 && xhr2.status == 200) {
//               var modifiedHtml = xhr2.responseText;
//               document.documentElement.innerHTML = modifiedHtml;
//             }
//           };
//           xhr2.send(html);
//         }
//       };
//       xhr.send();
//     });
//   });
// });
