function getDistance(xA, yA, xB, yB) { 
	var xDiff = xA - xB; 
	var yDiff = yA - yB;

    var distance = Math.sqrt(xDiff * xDiff + yDiff * yDiff);
	return distance;
}

document.querySelector('#find-distance').addEventListener(getDistance);