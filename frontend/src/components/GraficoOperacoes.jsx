import { React, Fragment } from "react";
import { useTheme } from "@mui/material/styles";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Label,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import Title from "./Title";

export default function Chart({ data }) {
  const theme = useTheme();

  let resultado = data
    .filter((objeto) => objeto.status === "Concluído")
    .map(({ type_operation, price_total }) => ({
      type_operation,
      price_total,
    }))
    .slice(0, 10)
    .reverse();

  return (
    <Fragment>
      <Title>Análise</Title>
      <ResponsiveContainer>
        <LineChart
          data={resultado}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="type_operation"
            stroke={theme.palette.text.secondary}
            style={theme.typography.body2}
          />
          <YAxis
            stroke={theme.palette.text.secondary}
            style={theme.typography.body2}
          >
            <Label
              angle={270}
              position="left"
              style={{
                textAnchor: "middle",
                fill: theme.palette.text.primary,
                ...theme.typography.body1,
              }}
            >
              Transações ($)
            </Label>
          </YAxis>
          <Tooltip />

          <Line
            isAnimationActive={false}
            type="monotone"
            dataKey="price_total"
            stroke={theme.palette.primary.main}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </Fragment>
  );
}
