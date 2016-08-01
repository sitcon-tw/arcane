$(document).ready(function() {
	//資料
	var dd = [];
	$('.point').each(function() {
		var t_id = $(this).find("td").eq(0).text();
		var t_point = $(this).find("td").eq(1).text();
		dd.push({ "name": t_id, "point": t_point });
		console.log(dd);
	});

	//新增一個SVG，並設定長、寬
	var svg = d3.select("#graph").append("svg")
		.attr("width", '100%')
		.attr("height", 400)
		.append("g")
		//因為原點座標0,0在左上角，所以必須位移到指定的位置上，
		//否則會因為在畫圓時，圓心座標在0,0而導致部份圖形被裁切。
		//位移就是在原本的座標上加上移動的數值。
		.attr("transform", "translate(250,250)");
	//定義顏色
	var color = d3.scale.ordinal()
		.range(["#2961fc", "#f2d33f", "#9ccf5f", "#3dc6e4", "#8096a4", "#c1628d"]);

	//繪製圖餅圖，必備的三個：
	//d3.svg.arc()
	//d3.layout.pie()
	//.append("path")

	//利用arc來產生圓形的accessor函數，
	//函數包含有內、外圓的角度起迄，
	//內、外圓的半徑
	var arc1 = d3.svg.arc()
		//設定內、外圓形的半徑大小
		.outerRadius(200)
		.innerRadius(100);

	//建立一個layout pie物件，無排序
	var pie = d3.layout.pie()
		.value(function(d) {
			return d.point; })
		.sort(null);

	var g1 = svg.selectAll("g")
		.data(pie(dd))
		.enter()
		.append("g")
		.attr('class', 'slice');
	//實際畫圓的方式是以SVG圖形路徑（Path）來繪製
	g1.append("path")
		//路徑的部份要設定在d屬性中，所以套入arc1函數，
		//d3.js會依據資料配合arc1函數產出Path所需的路徑
		.attr("d", arc1)
		.style("fill", function(d, i) {
			return color(i);
		});
	g1.append("text") //add a label to each slice
		.attr("transform", function(d) { //set the label's origin to the center of the arc
			//we have to make sure to set these before calling arc.centroid
			return "translate(" + arc1.centroid(d) + ")"; //this gives us a pair of coordinates like [50, 50]
		})
		.attr("text-anchor", "middle") //center the text on it's origin
		.attr("font-size", "16px") //center the text on it's origin
		.text(function(d) {
			return d.data.name + d.data.point; });
});
