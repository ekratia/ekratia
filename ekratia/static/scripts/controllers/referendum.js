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
  .controller('ReferendumController',
    ['$scope', '$ngBootbox', '$window',
    function ($scope, $ngBootbox, $window) {
        $scope.referendumId = null;
        $scope.referendumInit = function(referendumId, openURL){
            $scope.referendumId = referendumId;
            $scope.customDialogOptions.title = 'Open referendum ' + referendumId +' for voting';
            $scope.openURL = openURL;
        };

        $scope.customDialogOptions = {
            message: 'The referendum will be open for voting for 72 hours after you click the button below.',
            title: '',
            onEscape: function() {
            },
            show: true,
            backdrop: true,
            closeButton: true,
            animate: true,
            className: 'test-class',
            buttons: {
                cancel: {
                    label: "Cancel",
                    className: "btn-default",
                    callback: function() {  }
                },
                open: {
                    label: "Open for Voting Now",
                    className: "btn-primary",
                    callback: function() {
                        $window.location.href = $scope.openURL;
                    }
                }
            }
        };

        $scope.openVoting = function(){
            $ngBootbox.customDialog($scope.customDialogOptions);

        };
    }]);