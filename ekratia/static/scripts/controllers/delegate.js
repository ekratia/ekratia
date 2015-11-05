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
    ['$scope', 'AvailableDelegate', 'AssignedDelegate', 'User',
    function ($scope, AvailableDelegate, AssignedDelegate, User) {
        $scope.delegates = [];
        $scope.filter_name = '';
        $scope.user = null;
        $scope.current_user_id = null;

        $scope.init = function(current_user_id){
            $scope.current_user_id = current_user_id;
            $scope.loadDelegates();
        };

        $scope.loadDelegates = function(){
            $scope.loadAssignedDelegates();
            $scope.loadAvailableDelegates();
        }

        $scope.loadAssignedDelegates = function(){
            var data = AssignedDelegate.query(function(){
                $scope.assigned_delegates = data;
                var user_data = User.get({id:$scope.current_user_id},function(){
                    $scope.user = user_data;
                });
            });
        };

        $scope.loadAvailableDelegates = function(){
            var data = AvailableDelegate.query({name:$scope.filter_name},function(){
                $scope.available_delegates = data;
            });
        };

        $scope.addDelegate = function(user){
            AssignedDelegate.save({delegate:user.id},function(data){
                $scope.assigned_delegates.push(user);
                var idx = $scope.available_delegates.indexOf(user);
                $scope.available_delegates.splice(idx,1);
                // Needed to show new weight value
                $scope.loadAssignedDelegates();
                $scope.loadAvailableDelegates();
            });

        };

        $scope.undelegate = function(user){
            AssignedDelegate.delete({id:user.id},function(data){
                $scope.available_delegates.push(user);
                var idx = $scope.assigned_delegates.indexOf(user);
                $scope.assigned_delegates.splice(idx,1);
                // Needed to show new weight value
                $scope.loadAssignedDelegates();
                $scope.loadAvailableDelegates();
            });
        };

        $scope.filter_users = function(){
            
        }
    
}]);