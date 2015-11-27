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
  .controller('TrendingController',
    ['$scope', 'Conversation', 'Referendum',
    function ($scope, Conversation, Referendum) {

         Conversation.query(function(data){
            $scope.conversations = data.results;
         });

         Referendum.query(function(data){
            $scope.referendums = data.results;
         });
}]);