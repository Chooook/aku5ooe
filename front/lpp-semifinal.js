const userLoginsObject = {
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge',
  'login': 'judge'
}


var prefix = window.location.pathname.substr( 0, window.location.pathname.toLowerCase().lastIndexOf( "/extensions" ) + 1 );
var config = {
	host: window.location.hostname,
	prefix: prefix,
	port: window.location.port,
	isSecure: window.location.protocol === "https:"
};


// function formatAKUCheckboxes(checkboxes) {
// 	return Object.keys(checkboxes.participants).map(el => {
// 		const result = []
// 		result.push(checkboxes.participants[el]['like']);
// 		result.push(checkboxes.participants[el]['dislike']);
// 		return result
// 	})
// }  

require.config( {
	baseUrl: (config.isSecure ? "https://" : "http://") + config.host + (config.port ? ":" + config.port : "") + config.prefix + "resources"
} );



require( ["js/qlik"], (qlik) => {
	qlik.on( "error", (error) => {
		$( '#popupText' ).append(error.message + "<br>" );
		$( '#popup' ).fadeIn( 1000 );
	} );
	$( "#closePopup" ).click( function () {
		$( '#popup' ).hide();
	} );
	
	var app = qlik.sessionAppFromApp('7ccc2d81-ccc5-4b35-8d27-40230e0c38df');
	var global = app.global;

	var serverName = "AKU5";
	var sseScriptName = "OOEContest.OOEContest"
	var userLogin = localStorage.getItem('login') || fetchUserLogin();
	if (localStorage.getItem('login')) {
	console.log('here')
	  const userLoginBlock = document.querySelector('#content0');
	  userLoginBlock.textContent = `Добрый день, ${userLoginsObject[userLogin] || 'неизвестный пользователь'}`;
	}
	

	var scriptExpressions = {
		get_judge_data: {
			method: "get_judge_data",
			methodArgs: { userLogin: userLogin }
		},
		update_votes: {
			method: "update_votes",
			methodArgs: { userLogin: userLogin, newData : {} }
		},
		finish_voting: {
			method: "finish_voting",
			methodArgs: { userLogin: userLogin }
		}
	};

  	function fetchUserLogin() {
	console.log('here')
  		return global.getAuthenticatedUser()
 			.then(response => {
 				const user = response.qReturn;
 				userLogin = user.split(';')[1].split('=')[1];
				const userLoginBlock = document.querySelector('#content0');
	            userLoginBlock.textContent = `Добрый день, ${userLoginsObject[userLogin] || 'неизвестный пользователь'}`;
				localStorage.setItem('login', userLogin);
				return userLogin;

 			}).catch((error) => {
 				window.alert('Ошибка при получении логина пользователя!', error.message);
 				throw error;
 			});
  	}


	const checkboxButtons = document.querySelectorAll('[id^="checkbox"]');
//	checkboxButtons.forEach(button => {
//	    button.addEventListener('click', function(event) { handleCheckboxClick(event); });
//	});


	function handleCheckboxClick(event) {
		let button = event.target;
//		button.disabled = true;
		let method = "update_votes"

		updateScriptArg(scriptExpressions, method, {methodArgs: { userLogin: userLogin, newData: button.id }})
			.then(() => createScriptString(scriptExpressions, method))
			.then(scriptString => createCubeDefinition(undefined, [{formula: scriptString}], 1, [-1]))
			.then(cubeDef => createCube(cubeDef))
			.then(reply => updateVotes(reply))
			.then(reply => destroyCube(reply.qInfo.qId))
			.catch(error => console.error('Ошибка при создании папки задачи', error));
	}

//	function getFiniteValue(obj) {
//		getProp(obj);
//		function getProp(o) {
//			for(var prop in o) {
//				if(typeof(o[prop]) === 'object') {
//					getProp(o[prop]);
//				} else {
//					window.alert(o[prop])
//				}
//			}
//		}
//	}

	function updateVotes(reply) {
		let judgeData = reply.qHyperCube.qDataPages[0].qMatrix[0][0].qText;
		window.alert(judgeData)
//		ДОПИСАТЬ ПЕРЕНАЗНАЧЕНИЕ ПЕРЕМЕННЫХ
		return reply;
	}

	function handleGetJudgeData() {
		var method = "get_judge_data"
		updateScriptArg(scriptExpressions, method, {methodArgs: { userLogin: userLogin }})
			.then(() => createScriptString(scriptExpressions, method))
			.then(scriptString => createCubeDefinition(undefined, [{formula: scriptString}], 1, [-1]))
			.then(cubeDef => createCube(cubeDef))
			.then(reply => updateVotes(reply))
			.then(reply => destroyCube(reply.qInfo.qId))
			.catch(error => console.error('Ошибка при создании папки задачи', error));
	}

	function updateScriptArg(scriptExpressions, scriptKey, updates) {
		return new Promise((resolve, reject) => {
			if (scriptExpressions[scriptKey]) {
				Object.entries(updates).forEach(([argType, args]) => {
					if (scriptExpressions[scriptKey][argType]) {
						Object.entries(args).forEach(([argKey, value]) => {
							scriptExpressions[scriptKey][argType][argKey] = value;
						});
					}
				});
				resolve();
			} else {
				reject(new Error("Ошибка при обновлении значений в конфиге скрипта для SSE."));
			}
		});
	}

	function createScriptString(scriptExpressions, scriptKey) {
		return new Promise((resolve, reject) => {
			const scriptConfig = scriptExpressions[scriptKey];
			if (!scriptConfig) {
				reject(new Error("Не найден конфиг для указанного метода скрипта."));
			}
			// Преобразование аргументов методы в строку
			const methodArgsStr = scriptConfig.methodArgs
				? Object.entries(scriptConfig.methodArgs)
					.map(([key, value]) => `"${value}"`)
					.join(', ')
				: '';
			// Формирование строки с вызовом метода
			const methodInvocation = methodArgsStr ? `${scriptConfig.method}(${methodArgsStr})` : `${scriptConfig.method}()`;
			let scriptString = `${serverName}.ScriptEvalStr('${sseScriptName}().${methodInvocation}')`;
			resolve(scriptString);
		});
	}

	function createCubeDefinition(dimensions = [], measures = [], initialDataFetchSize = 1000, sortOrders = []) {
		return new Promise((resolve, reject) => {
			let cubeDefinition = {
				qDimensions: dimensions.map(dimension => ({
					qDef: { qFieldDefs: [dimension.field], qSortCriterias: [dimension.sortCriteria || {}] },
					qNullSuppression: dimension.nullSuppression || false
				})),
				qMeasures: measures.map(measure => ({
					qDef: { qDef: measure.formula, qSortBy: measure.sortBy || {} },
					qLabel: measure.label || "",
					qFormat: measure.format || { qType: "U", qnDec: 0, qUseThou: 0 }
				})),
				qInitialDataFetch: [{
					qWidth: dimensions.length + measures.length,
					qHeight: initialDataFetchSize
				}],
				qInterColumnSortOrder: sortOrders,
				qSuppressZero: false,
				qSuppressMissing: true
			}
			resolve(cubeDefinition);
		}).catch((error) => {
			throw new Error('Ошибка при формировании definition куба данных', error);
		})
	}

	function createCube(cubeDefinition) {
		return new Promise((resolve, reject) => {
			app.createCube(cubeDefinition, function(reply) {
				if (reply.qHyperCube) {
					//console.log(reply)
					resolve(reply);
				} else {
					reject('Ошибка при создании куба');
				}
			}).catch(error => {
				reject('Ошибка при создании куба' + error.message);
			});
		});
	}

	function destroyCube(cubeId) {
		app.destroySessionObject(cubeId)
			.then(function() {
				console.log(`Куб ${cubeId} удален!`);
			}).catch(function(error) {
				console.error('Ошибка при удалении куба', error);
				throw new Error(error);
			});
	}

} );
