import { View, Text, TextInput, StyleSheet } from "react-native";
import React from "react";
import { Controller } from "react-hook-form";
const CustomInput = ({
  control,
  name,
  rules = {},
  placeholder,
  secureTextEntry,
}) => {
  return (
    <Controller
      control={control}
      name={name}
      rules={rules}
      render={({
        field: { value, onChange, onBlur },
        fieldState: { error },
      }) => (
        <>
          <View
            style={[
              styles.container,
              { borderColor: error ? "red" : "#e8e8e8" },
            ]}
          >
            <TextInput
              value={value}
              onBlur={onBlur}
              onChangeText={onChange}
              placeholder={placeholder}
              style={styles.input}
              secureTextEntry={secureTextEntry}
            ></TextInput>
          </View>
          {error && (
            <Text style={{ color: "red", alignSelf: "stretch" }}>
              {error.message || "error"}
            </Text>
          )}
        </>
      )}
    />
  );
};
const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    width: "100%",
    borderColor: "#e8e8e8",
    borderWidth: 1,
    height: 30,
    borderRadius: 5,
    paddingHorizontal: 10,
    marginVertical: 8,
  },
  input: {},
});

export default CustomInput;
