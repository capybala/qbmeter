(function() {
  'use strict';

  var d = document;
  var storeId = location.href.match(/[?&]id=(\d+)/)[1];

  // Clear existing elements
  Array.prototype.forEach.call(d.querySelectorAll('.qbmeter'), function(element) {
    element.parentNode.removeChild(element);
  });

  // Create style element
  var style = d.createElement('style');
  style.classList.add('qbmeter');
  style.appendChild(d.createTextNode('\
.qbmeter { border-spacing: none; border-collapse: collapse;} \
.qbmeter th {border: 1px solid gray; width: 40px;  text-align: center;} \
.qbmeter td {border: 1px solid gray; background-color: lightgray; width: 50px; height: 18px;} \
'));

  // Create table element without data
  var createTable = function(storeId) {
    var table = d.createElement('table');
    table.classList.add('qbmeter');

    var thead = d.createElement('thead');
    var tr = d.createElement('tr');
    thead.appendChild(tr);
    ['時刻', '日', '月', '火', '水', '木', '金', '土'].forEach(function(label) {
      var th = d.createElement('th');
      th.appendChild(d.createTextNode(label));
      tr.appendChild(th);
    });

    table.appendChild(thead);

    var tbody = d.createElement('tbody');
    table.appendChild(tbody);

    for (var h = 8; h < 23; h++) {
      var hour = ('0' + h).slice(-2);
      ['00', '30'].forEach(function(minute) {
        var tr = d.createElement('tr');
        if (minute == '00') {
          var th = d.createElement('th');
          th.rowSpan = 2;
          th.appendChild(d.createTextNode(hour));
          tr.appendChild(th);
        }

        for (var w = 0; w < 7; w++) {
          var td = d.createElement('td');
          td.id = 'qbmeter-' + storeId + '-' + hour + minute + '-' + w;
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      });
    }

    return table;
  };
  var table = createTable(storeId);

  // Insert the elements into DOM
  // #box_store-avail is for PC, .box_store-avail is for mobile
  var before = d.querySelector('#box_store-avail, .box_store-avail');
  before.parentNode.insertBefore(style, before.nextSibling);
  before.parentNode.insertBefore(table, before.nextSibling);

  // Request congestion data
  var xhr = new XMLHttpRequest();
  xhr.addEventListener('load', function() {
    if (this.status == 200) {
      loaded(JSON.parse(this.responseText));
    }
  });
  xhr.open('GET', 'https://orangain.cloudant.com/qbmeter/' + storeId);
  xhr.send();

  // Set color of table cells
  var loaded = function(store) {
    var storeId = store._id;
    store.congestions.forEach(function(congestion) {
      var id = 'qbmeter-' + storeId + '-' + congestion.timebox + '-' + congestion.day_of_week;
      var td = d.getElementById(id);
      var red = Math.floor(Math.min(0.5, congestion.congestion) * 2 * 255);
      var green = Math.floor(255 - Math.max(0, congestion.congestion - 0.5) * 2 * 255);
      var color = 'rgb(' + red + ',' + green + ', 0)';
      td.style.backgroundColor = color;
    });

  };
})();
