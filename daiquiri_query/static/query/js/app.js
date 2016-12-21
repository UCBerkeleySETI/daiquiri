var app = angular.module('query', ['core']);

app.filter('bytes', function() {
    return function(bytes) {
        if (angular.isUndefined(bytes) || isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '';
        if (bytes === 0 || bytes === '0' ) return '0 bytes';

        var units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'];
        var number = Math.floor(Math.log(bytes) / Math.log(1024));

        return (bytes / Math.pow(1024, Math.floor(number))).toFixed(1) +  ' ' + units[number];
    };
});

app.controller('QueryController', ['$scope', 'QueryService', function($scope, QueryService) {

    $scope.service = QueryService;
    $scope.service.init();
}]);
