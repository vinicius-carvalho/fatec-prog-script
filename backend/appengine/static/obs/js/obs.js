var Obsmodulo = angular.module('Obsmodulo',[]);


Obsmodulo.directive('obsform',function(){
    return{
        restrict:'E',
        replace:true,
        scope:{},
        templateUrl:'/static/obs/html/form.html',

        controller:['$scope','$http', function($scope,$http){
            $scope.obs={setor:'',linha:'',data:'',comportamento:'', nome:''};
            $scope.salvando=false;
            $scope.erros={};

            $scope.salvar = function() {

                    $scope.erros={};
                   var promessa = $http.post('/observacoes/rest/save', $scope.obs);
                    $scope.salvando = true;


                    promessa.success(function (obs_servidor) {
                        $scope.salvando=false;
                        console.log('aqui', obs_servidor);
                        $scope.obs = {};
                    });



                    promessa.error(function (erros) {
                        $scope.erros = erros;
                        console.log('erro',erros);
                        $scope.salvando=false;
                        });


                }

        }]

    };
});
