import { View, Text, StyleSheet } from "react-native";
import React, { useState } from "react";
import Custombutton from "../../Components/Custombutton";
import Custominput from "../../Components/Custominput";
import { useNavigation } from "@react-navigation/native";
import { useForm } from "react-hook-form";
import axios from "axios";

const ResetPassword = ({ route, navigation }) => {
  const email = route.params;
  const x = email.email.email;
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onConfirmPressed = async (data) => {
    const y = data.code;
    const user = {
      email: "",
      code: "",
    };
    user.email = x;
    user.code = y;
    await axios
      .post(`http://192.168.56.1:5000/mobapp/confirm`, user)
      .then((resp) => {
        navigation.navigate("NewPassword", {
          email: x,
          code: y,
        });
      })
      .catch((err) => alert("The code is not correct"));
  };
  const onSendPressed = async () => {
    await axios
      .patch(`http://192.168.56.1:5000/mobapp`, email.email)
      .then((resp) => {
        alert("The code has been sent again");
      })
      .catch((err) => alert("There is no such email"));
  };
  return (
    <View style={Styles.root}>
      <Text style={Styles.title}>Confirm your email</Text>
      <Custominput placeholder="code" control={control} name="code" />

      <Custombutton
        text="Confirm"
        onPress={handleSubmit(onConfirmPressed)}
        type="SECONDARY"
      ></Custombutton>
      <Custombutton
        text="Send Again"
        onPress={handleSubmit(onSendPressed)}
        type="PRIMARY"
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

export default ResetPassword;
