'use strict';

/**
 * @ngdoc function
 * @name frontApp.controller:CommentsController
 * @description
 * # CommentsController
 * Controller of the application
 * Handles information from the API to be connected with the view
 */
angular.module('Ekratia')
  .controller('DelegatesController',
    ['$scope',
    function ($scope) {
        $scope.delegates = [];

        $scope.loadDelegates = function(){
            $scope.delegates = [
            {"user": {"username": "Andres Gonzalez", avatar: 'http://placehold.it/75x75/'}},
            {"user": {"username": "William Perez", avatar: 'http://placehold.it/75x75/'}},
            {"user": {"username": "William Perez", avatar: 'http://placehold.it/75x75/'}},
            {"user": {"username": "William Perez", avatar: 'http://placehold.it/75x75/'}},
            {"user": {"username": "William Perez", avatar: 'http://placehold.it/75x75/'}},
            ];
        };

        $scope.addDelegate = function(){
            $scope.delegates.push({"user": {"username": "New Delegate", avatar: 'http://placehold.it/75x75/'}});
        };

        $scope.undelegate = function(item){
            var idx = $scope.delegates.indexOf(item);
            $scope.delegates.splice(idx,1);
        };

    
}]);