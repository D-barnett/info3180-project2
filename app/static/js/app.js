var app = angular.module('Appliancewishlist', []);

app.controller('MainController', function($scope, $http) {
    $http.get("http://info3180-project2-d-barnett.c9users.io/api/thumbnails")
    .then(function(response) {
        $scope.products = response.data['getimages'];
    });
});