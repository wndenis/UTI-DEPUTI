(function () {
  var CITIES = ['RU.SP', 'RU.MS.CITY'];

  var WIDTH_DEFAULT = 920;
  var HEIGHT_DEFAULT = 500;
  var SCALE_DEFAULT = 700;

  var rusmap = function (options) {
    options || (options = {});

    var container = options.el ? d3.select(options.el) : d3.select('body');
    var width = options.width || WIDTH_DEFAULT;
    var height = options.height || HEIGHT_DEFAULT;
    var mapUrl = options.mapUrl || 'russian.json';
    var dataUrl = options.dataUrl || 'codes.json';

    var scale = Math.min(
      SCALE_DEFAULT * width / WIDTH_DEFAULT,
      SCALE_DEFAULT * height / HEIGHT_DEFAULT
    );
  
    // Albers Siberia projection
    var projection = d3.geo.albers()
      .rotate([-105, 0])
      .center([-10, 65])
      .parallels([52, 64])
      .scale(scale)
      .translate([width / 2, height / 2]);

    var path = d3.geo.path().projection(projection);

    var svg = container.append('svg')
      .attr('xmlns', 'http://www.w3.org/2000/svg')
      .attr('xmlns:xlink', 'http://www.w3.org/1999/xlink')
      .attr('class', 'map')
      .attr('width', width)
      .attr('height', height);

    queue()
      .defer(d3.json, mapUrl)
      .defer(d3.json, dataUrl)
      .await(function (error, russia, codes) {
        if (error) {
          console.error(error);
          return;
        }

        render(russia, codes);
      });

    function render(russia, codes) {
      var regions = topojson.feature(russia, russia.objects.regions);

      regions.features = regions.features.sort(function (first, second) {
        var firstScore = CITIES.indexOf(first.id) === -1 ? 1 : 0;
        var secondScore = CITIES.indexOf(second.id) === -1 ? 1 : 0;
        return secondScore - firstScore;
      });

      // .map__region-boundary
      svg.append('path')
        .datum(topojson.merge(russia, russia.objects.regions.geometries))
        .attr('d', path)
        .attr('class', 'map__region-boundary');

      // .map__region-boundary_inner
      svg.append('path')
        .datum(topojson.mesh(russia, russia.objects.regions, function (a, b) { return a !== b; }))
        .attr('d', path)
        .attr('class', 'map__region-boundary map__region-boundary_inner');

      // .map__region
      var links = svg.selectAll('.map__region')
          .data(regions.features)
        .enter().append('a')
          .attr('class', 'map__region')
          .attr('xlink:href', function (d) { return codes[d.id].link; });
          //.attr('target', '_blank');

      // .map__region path
      links.append('path')
        .attr('data-code', function (d) { return d.id; })
        .attr('fill', function (d) { return codes[d.id].color; })
        .attr('d', path);

      // .map__place-label
      links.each(function (d) {
        if (CITIES.indexOf(d.id) !== -1) {
          var el = d3.select(this);

          el.append('text')
            .attr('class', 'map__place-label')
            .attr('data-code', function (d) { return d.id; })
            .attr('transform', function (d) { return 'translate(' + path.centroid(d) + ')'; })
            .attr('x', 6)
            .attr('dy', '.35em')
            .style('text-anchor', 'start')
            .text(function (d) { return codes[d.id].name; });

          el.append('circle')
            .attr('data-code', function (d) { return d.id; })
            .attr('cx', function (d) { return path.centroid(d)[0]; })
            .attr('cy', function (d) { return path.centroid(d)[1]; })
            .attr('r', 4)
            .style('fill', function(d) { return '#FF9922'; });
        }
      });

      // .tooltip
      var tooltip = svg.append('text')
        .attr('class', 'map__tooltip')
        .attr('x', 15)
        .attr('dy', '.35em')
        .attr('transform', 'translate(0,' + (height * 0.9) + ')');

      // events
      svg.on('mousemove', function () {
        var el = d3.select(d3.event.target);
        var code = el.attr('data-code');

        if (code) {
          // show
          tooltip.text(codes[code].name);
        } else {
          // hide
          tooltip.text('');
        }
      });
    }
  };

  var $ = window.jQuery;
  if ($) {
    $.fn.rusmap = function (options) {
      rusmap($.extend({}, options, {
        el: this.get(0)
      }));

      return this;
    };
  }

  window.rusmap = rusmap;
})();