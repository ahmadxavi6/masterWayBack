import { View, Text, StyleSheet } from "react-native";
import React, { useState } from "react";
import Custombutton from "../../Components/Custombutton";
import Custominput from "../../Components/Custominput";
import { useNavigation, navigation } from "@react-navigation/native";
import { useForm } from "react-hook-form";
import axios from "axios";
const ForgotPassword = ({ navigation }) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();
  // const navigation = useNavigation();
  const onForgotPasswordPressed = async (data) => {
    await axios
      .patch(`http://192.168.56.1:5000/mobapp`, data)
      .then((resp) => {
        alert("Reset Password Email has been sent");
        navigation.navigate("ResetPassword", {
          email: data,
        });
      })

      .catch((err) => alert("There is no such email"));
  };

  return (
    <View style={Styles.root}>
      <Text style={Styles.title}>Reset your password</Text>
      <Custominput
        placeholder={"Email"}
        rules={{ required: "Email is Required" }}
        placeholder="Email"
        control={control}
        name="email"
      />

      <Custombutton
        text="Send Reset Password Email"
        onPress={handleSubmit(onForgotPasswordPressed)}
        type="SECONDARY"
      ></Custombutton>
    </View>
  );
};
const Styles = StyleSheet.create({
  root: {
    alignItems: "center",
    padding: 20,
  },
  logo: {
    width: "70%",
    maxWidth: 300,
    maxHeight: 300,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#051c60",
    margin: 10,
  },
});

export default ForgotPassword;
