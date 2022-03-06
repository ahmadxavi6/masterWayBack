import { View, Text } from "react-native";
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Signin from "../Screens/Signin";
import Resetpassword from "../Screens/Resetpassword";
import Forgotpassword from "../Screens/Forgotpassword";
import NewPassword from "../Screens/NewPassword";
import Home from "../Screens/Home";
const Stack = createNativeStackNavigator();

const Navigation = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="SignIn" component={Signin}></Stack.Screen>
        <Stack.Screen
          name="ResetPassword"
          component={Resetpassword}
        ></Stack.Screen>
        <Stack.Screen
          name="ForgotPassword"
          component={Forgotpassword}
        ></Stack.Screen>
        <Stack.Screen name="Home" component={Home}></Stack.Screen>
        <Stack.Screen name="NewPassword" component={NewPassword}></Stack.Screen>
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default Navigation;
