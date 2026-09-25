# import pandas as pd

# from app.repositories.sales_repository import (
#     get_dataset,
#     get_payments,
# )

# from app.services.kpi_service import (
#     CATEGORY_TRANSLATIONS,
#     PAYMENT_TRANSLATIONS,
# )


# async def get_business_insights(dataset_id="olist", user_id=None):
#     df = await get_dataset(
#         dataset_id,
#         user_id,
#     )

#     if df.empty:
#         return {
#             "dataset_id": dataset_id,
#             "insights": [],
#         }

#     insights = []

#     # Revenue Trend
#     if dataset_id == "olist":
#         revenue_column = "item_total"
#     else:
#         revenue_column = "revenue"

#     if revenue_column in df.columns:
#         revenue = pd.to_numeric(
#             df[revenue_column],
#             errors="coerce",
#         ).dropna()

#         if len(revenue) >= 2:
#             first_revenue = float(revenue.iloc[0])
#             last_revenue = float(revenue.iloc[-1])

#             if first_revenue != 0:
#                 change_percent = (
#                     (last_revenue - first_revenue) / abs(first_revenue)
#                 ) * 100

#                 if change_percent > 0:
#                     message = (
#                         f"Revenue increased by "
#                         f"{change_percent:.1f}% from the beginning "
#                         f"to the end of the dataset."
#                     )
#                 elif change_percent < 0:
#                     message = (
#                         f"Revenue decreased by "
#                         f"{abs(change_percent):.1f}% from the beginning "
#                         f"to the end of the dataset."
#                     )
#                 else:
#                     message = (
#                         "Revenue remained stable from the beginning "
#                         "to the end of the dataset."
#                     )

#                 insights.append(
#                     {
#                         "type": "revenue",
#                         "title": "Revenue Trend",
#                         "message": message,
#                     }
#                 )

#                 if change_percent >= 20:
#                     insights.append(
#                         {
#                             "type": "alert",
#                             "title": "Revenue Growth Alert",
#                             "message": (
#                                 f"Revenue increased by "
#                                 f"{change_percent:.1f}%. "
#                                 f"The business is showing strong "
#                                 f"revenue growth."
#                             ),
#                         }
#                     )

#                 if change_percent <= -20:
#                     insights.append(
#                         {
#                             "type": "alert",
#                             "title": "Revenue Decline Alert",
#                             "message": (
#                                 f"Revenue declined by "
#                                 f"{abs(change_percent):.1f}%. "
#                                 f"The business should review recent sales "
#                                 f"performance and identify factors contributing "
#                                 f"to the decline."
#                             ),
#                         }
#                     )

#     # Top Performing Category
#     if dataset_id == "olist":
#         category_column = "product_category_name"
#     else:
#         category_column = "category"

#     if category_column in df.columns and revenue_column in df.columns:
#         category_df = df.copy()

#         category_df[revenue_column] = pd.to_numeric(
#             category_df[revenue_column],
#             errors="coerce",
#         )

#         category_df = category_df.dropna(
#             subset=[
#                 category_column,
#                 revenue_column,
#             ]
#         )

#         if not category_df.empty:
#             category_revenue = (
#                 category_df.groupby(category_column)[revenue_column]
#                 .sum()
#                 .sort_values(ascending=False)
#             )

#             top_category = category_revenue.index[0]
#             top_category_revenue = category_revenue.iloc[0]
#             formatted_category_revenue = f"{top_category_revenue:,.2f}"

#             display_category = CATEGORY_TRANSLATIONS.get(
#                 top_category,
#                 str(top_category).replace("_", " ").title(),
#             )

#             insights.append(
#                 {
#                     "type": "category",
#                     "title": "Top Performing Category",
#                     "message": (
#                         f"{display_category} generated the highest revenue "
#                         f"with {formatted_category_revenue} in total sales."
#                     ),
#                 }
#             )

#         # Customer Activity
#     if dataset_id == "olist":
#         customer_column = "customer_unique_id"
#     else:
#         customer_column = "customers"

#     if customer_column in df.columns:
#         if dataset_id == "olist":
#             customer_count = df[customer_column].nunique()
#         else:
#             customer_count = pd.to_numeric(
#                 df[customer_column],
#                 errors="coerce",
#             ).sum()

#         insights.append(
#             {
#                 "type": "customers",
#                 "title": "Customer Activity",
#                 "message": (
#                     f"The dataset contains approximately "
#                     f"{int(customer_count):,} customers."
#                 ),
#             }
#         )

#         # Review Performance
#     if "review_score" in df.columns:
#         review_scores = pd.to_numeric(
#             df["review_score"],
#             errors="coerce",
#         ).dropna()

#         if not review_scores.empty:
#             average_review = float(review_scores.mean())

#             if average_review >= 4:
#                 review_message = (
#                     f"Customer satisfaction is strong with "
#                     f"an average review score of "
#                     f"{average_review:.1f} out of 5."
#                 )
#             elif average_review >= 3:
#                 review_message = (
#                     f"Customer satisfaction is moderate with "
#                     f"an average review score of "
#                     f"{average_review:.1f} out of 5."
#                 )
#             else:
#                 review_message = (
#                     f"Customer satisfaction needs attention with "
#                     f"an average review score of "
#                     f"{average_review:.1f} out of 5."
#                 )

#             insights.append(
#                 {
#                     "type": "reviews",
#                     "title": "Customer Satisfaction",
#                     "message": review_message,
#                 }
#             )

#             # Customer Satisfaction Recommendation
#             if average_review >= 4:
#                 recommendation = (
#                     "Maintain the current customer experience "
#                     "and continue focusing on service quality."
#                 )
#             elif average_review >= 3:
#                 recommendation = (
#                     "Focus on improving customer experience "
#                     "to increase overall satisfaction."
#                 )
#             else:
#                 recommendation = (
#                     "Customer satisfaction requires attention. "
#                     "Review product and service quality to identify "
#                     "the main causes of low ratings."
#                 )

#             insights.append(
#                 {
#                     "type": "recommendation",
#                     "title": "Business Recommendation",
#                     "message": recommendation,
#                 }
#             )

#         # Business Scale
#     if revenue_column in df.columns:
#         revenue_values = pd.to_numeric(
#             df[revenue_column],
#             errors="coerce",
#         ).dropna()

#         if not revenue_values.empty:
#             total_revenue = float(revenue_values.sum())

#             insights.append(
#                 {
#                     "type": "business_scale",
#                     "title": "Total Business Revenue",
#                     "message": (
#                         f"The dataset records a total revenue of "
#                         f"{total_revenue:,.2f}."
#                     ),
#                 }
#             )

#         # Average Order Value
#     if revenue_column in df.columns:
#         if dataset_id == "olist":
#             order_count = df["order_id"].nunique() if "order_id" in df.columns else 0
#         else:
#             order_count = (
#                 pd.to_numeric(
#                     df["orders"],
#                     errors="coerce",
#                 ).sum()
#                 if "orders" in df.columns
#                 else 0
#             )

#         revenue_values = pd.to_numeric(
#             df[revenue_column],
#             errors="coerce",
#         ).dropna()

#         if order_count > 0 and not revenue_values.empty:
#             total_revenue = float(revenue_values.sum())

#             average_order_value = total_revenue / order_count

#             insights.append(
#                 {
#                     "type": "average_order_value",
#                     "title": "Average Order Value",
#                     "message": (
#                         f"The average order value is " f"{average_order_value:,.2f}."
#                     ),
#                 }
#             )

#         # Most Used Payment Method
#     if dataset_id == "olist":
#         payments = await get_payments(
#             dataset_id,
#             user_id,
#         )

#         if "payment_type" in payments.columns and not payments.empty:
#             payment_counts = payments["payment_type"].dropna().value_counts()

#             if not payment_counts.empty:
#                 top_payment_method = payment_counts.index[0]

#                 payment_name = PAYMENT_TRANSLATIONS.get(
#                     top_payment_method,
#                     str(top_payment_method).replace("_", " ").title(),
#                 )

#                 insights.append(
#                     {
#                         "type": "payment",
#                         "title": "Most Used Payment Method",
#                         "message": (
#                             f"{payment_name} is the most frequently "
#                             f"used payment method in the dataset."
#                         ),
#                     }
#                 )

#     elif "payment_method" in df.columns:
#         payment_counts = df["payment_method"].dropna().value_counts()

#         if not payment_counts.empty:
#             top_payment_method = payment_counts.index[0]

#             payment_name = (
#                 str(top_payment_method)
#                 .replace(
#                     "_",
#                     " ",
#                 )
#                 .title()
#             )

#             insights.append(
#                 {
#                     "type": "payment",
#                     "title": "Most Used Payment Method",
#                     "message": (
#                         f"{payment_name} is the most frequently "
#                         f"used payment method in the dataset."
#                     ),
#                 }
#             )

#             # Business Opportunity
#         if category_column in df.columns and revenue_column in df.columns:
#             opportunity_df = df.copy()

#             opportunity_df[revenue_column] = pd.to_numeric(
#                 opportunity_df[revenue_column],
#                 errors="coerce",
#             )

#             opportunity_df = opportunity_df.dropna(
#                 subset=[
#                     category_column,
#                     revenue_column,
#                 ]
#             )

#             if not opportunity_df.empty:
#                 category_revenue = (
#                     opportunity_df.groupby(category_column)[revenue_column]
#                     .sum()
#                     .sort_values(ascending=False)
#                 )

#                 total_revenue = float(opportunity_df[revenue_column].sum())

#                 if not category_revenue.empty and total_revenue > 0:
#                     top_category = category_revenue.index[0]
#                     top_category_revenue = float(category_revenue.iloc[0])

#                     display_category = CATEGORY_TRANSLATIONS.get(
#                         top_category,
#                         str(top_category).replace("_", " ").title(),
#                     )

#                     revenue_share = (top_category_revenue / total_revenue) * 100

#                     if revenue_share >= 30:
#                         opportunity_message = (
#                             f"{display_category} contributes "
#                             f"{revenue_share:.1f}% of total revenue. "
#                             f"This category may be a strong candidate "
#                             f"for additional promotional focus."
#                         )

#                         insights.append(
#                             {
#                                 "type": "opportunity",
#                                 "title": "Growth Opportunity",
#                                 "message": opportunity_message,
#                             }
#                         )

#                     if revenue_share >= 50:
#                         insights.append(
#                             {
#                                 "type": "alert",
#                                 "title": "Business Alert",
#                                 "message": (
#                                     f"{display_category} contributes "
#                                     f"{revenue_share:.1f}% of total revenue. "
#                                     f"The business is highly dependent on "
#                                     f"this category."
#                                 ),
#                             }
#                         )

#             # Overall Business Interpretation
#     interpretation_parts = []

#     if category_column in df.columns and revenue_column in df.columns:
#         interpretation_df = df.copy()

#         interpretation_df[revenue_column] = pd.to_numeric(
#             interpretation_df[revenue_column],
#             errors="coerce",
#         )

#         interpretation_df = interpretation_df.dropna(
#             subset=[
#                 category_column,
#                 revenue_column,
#             ]
#         )

#         if not interpretation_df.empty:
#             category_revenue = (
#                 interpretation_df.groupby(category_column)[revenue_column]
#                 .sum()
#                 .sort_values(ascending=False)
#             )

#             total_revenue = float(interpretation_df[revenue_column].sum())

#             if not category_revenue.empty and total_revenue > 0:
#                 top_category = category_revenue.index[0]

#                 if dataset_id == "olist":
#                     top_category = CATEGORY_TRANSLATIONS.get(
#                         top_category,
#                         str(top_category).replace("_", " ").title(),
#                     )
#                 top_category_revenue = float(category_revenue.iloc[0])

#                 revenue_share = (top_category_revenue / total_revenue) * 100

#                 interpretation_parts.append(
#                     f"{top_category} is the leading revenue category, "
#                     f"contributing {revenue_share:.1f}% of total revenue."
#                 )

#     if revenue_column in df.columns:
#         revenue_values = pd.to_numeric(
#             df[revenue_column],
#             errors="coerce",
#         ).dropna()

#         if len(revenue_values) >= 2:
#             first_revenue = float(revenue_values.iloc[0])
#             last_revenue = float(revenue_values.iloc[-1])

#             if first_revenue != 0:
#                 change_percent = (
#                     (last_revenue - first_revenue) / abs(first_revenue)
#                 ) * 100

#                 if change_percent > 0:
#                     interpretation_parts.append(
#                         f"Revenue increased by {change_percent:.1f}% "
#                         f"from the beginning to the end of the dataset."
#                     )
#                 elif change_percent < 0:
#                     interpretation_parts.append(
#                         f"Revenue declined by {abs(change_percent):.1f}% "
#                         f"from the beginning to the end of the dataset."
#                     )
#                 else:
#                     interpretation_parts.append(
#                         "Revenue remained stable from the beginning "
#                         "to the end of the dataset."
#                     )

#     if "review_score" in df.columns:
#         review_scores = pd.to_numeric(
#             df["review_score"],
#             errors="coerce",
#         ).dropna()

#         if not review_scores.empty:
#             average_review = float(review_scores.mean())

#             if average_review >= 4:
#                 interpretation_parts.append("Customer satisfaction remains strong.")
#             elif average_review >= 3:
#                 interpretation_parts.append(
#                     "Customer satisfaction is moderate and " "could be improved."
#                 )
#             else:
#                 interpretation_parts.append("Customer satisfaction requires attention.")

#     if interpretation_parts:
#         insights.append(
#             {
#                 "type": "interpretation",
#                 "title": "Overall Business Interpretation",
#                 "message": " ".join(interpretation_parts),
#             }
#         )

#     return {
#         "dataset_id": dataset_id,
#         "insights": insights,
#     }






import pandas as pd

from app.repositories.sales_repository import (
    get_dataset,
    get_payments,
)

from app.services.kpi_service import (
    CATEGORY_TRANSLATIONS,
    PAYMENT_TRANSLATIONS,
)


async def get_business_insights(dataset_id="olist", user_id=None):
    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if df.empty:
        return {
            "dataset_id": dataset_id,
            "insights": [],
        }

    insights = []

    # Revenue Trend
    if dataset_id == "olist":
        revenue_column = "item_total"
    else:
        revenue_column = "revenue"

    if revenue_column in df.columns:
        revenue = pd.to_numeric(
            df[revenue_column],
            errors="coerce",
        ).dropna()

        if len(revenue) >= 2:
            first_revenue = float(revenue.iloc[0])
            last_revenue = float(revenue.iloc[-1])

            if first_revenue != 0:
                change_percent = (
                    (last_revenue - first_revenue) / abs(first_revenue)
                ) * 100

                if change_percent > 0:
                    message_key = "revenueIncreasedMessage"
                elif change_percent < 0:
                    message_key = "revenueDecreasedMessage"
                else:
                    message_key = "revenueStableMessage"

                insights.append(
                    {
                        "type": "revenue",
                        "title_key": "revenueTrendTitle",
                        "message_key": message_key,
                        "params": {
                            "percentage": f"{abs(change_percent):.1f}",
                        },
                    }
                )

                if change_percent >= 20:
                    insights.append(
                        {
                            "type": "alert",
                            "title_key": "revenueGrowthAlertTitle",
                            "message_key": "revenueGrowthAlertMessage",
                            "params": {
                                "percentage": f"{change_percent:.1f}",
                            },
                        }
                    )

                if change_percent <= -20:
                    insights.append(
                        {
                            "type": "alert",
                            "title_key": "revenueDeclineAlertTitle",
                            "message_key": "revenueDeclineAlertMessage",
                            "params": {
                                "percentage": f"{abs(change_percent):.1f}",
                            },
                        }
                    )

    # Top Performing Category
    if dataset_id == "olist":
        category_column = "product_category_name"
    else:
        category_column = "category"

    if category_column in df.columns and revenue_column in df.columns:
        category_df = df.copy()

        category_df[revenue_column] = pd.to_numeric(
            category_df[revenue_column],
            errors="coerce",
        )

        category_df = category_df.dropna(
            subset=[
                category_column,
                revenue_column,
            ]
        )

        if not category_df.empty:
            category_revenue = (
                category_df.groupby(category_column)[revenue_column]
                .sum()
                .sort_values(ascending=False)
            )

            top_category = category_revenue.index[0]
            top_category_revenue = category_revenue.iloc[0]
            formatted_category_revenue = f"{top_category_revenue:,.2f}"

            display_category = CATEGORY_TRANSLATIONS.get(
                top_category,
                str(top_category).replace("_", " ").title(),
            )

            insights.append(
                {
                    "type": "category",
                    "title_key": "topPerformingCategoryTitle",
                    "message_key": "topPerformingCategoryMessage",
                    "params": {
                        "category": display_category,
                        "revenue": formatted_category_revenue,
                    },
                }
            )

    # Customer Activity
    if dataset_id == "olist":
        customer_column = "customer_unique_id"
    else:
        customer_column = "customers"

    if customer_column in df.columns:
        if dataset_id == "olist":
            customer_count = df[customer_column].nunique()
        else:
            customer_count = pd.to_numeric(
                df[customer_column],
                errors="coerce",
            ).sum()

        insights.append(
            {
                "type": "customers",
                "title_key": "customerActivityTitle",
                "message_key": "customerActivityMessage",
                "params": {
                    "customers": f"{int(customer_count):,}",
                },
            }
        )

    # Review Performance
    if "review_score" in df.columns:
        review_scores = pd.to_numeric(
            df["review_score"],
            errors="coerce",
        ).dropna()

        if not review_scores.empty:
            average_review = float(review_scores.mean())

            if average_review >= 4:
                review_message_key = "customerSatisfactionStrongMessage"
                recommendation_key = "businessRecommendationStrongMessage"
            elif average_review >= 3:
                review_message_key = "customerSatisfactionModerateMessage"
                recommendation_key = "businessRecommendationModerateMessage"
            else:
                review_message_key = "customerSatisfactionAttentionMessage"
                recommendation_key = "businessRecommendationAttentionMessage"

            insights.append(
                {
                    "type": "reviews",
                    "title_key": "customerSatisfactionTitle",
                    "message_key": review_message_key,
                    "params": {
                        "score": f"{average_review:.1f}",
                    },
                }
            )

            # Customer Satisfaction Recommendation
            insights.append(
                {
                    "type": "recommendation",
                    "title_key": "businessRecommendationTitle",
                    "message_key": recommendation_key,
                }
            )

    # Business Scale
    if revenue_column in df.columns:
        revenue_values = pd.to_numeric(
            df[revenue_column],
            errors="coerce",
        ).dropna()

        if not revenue_values.empty:
            total_revenue = float(revenue_values.sum())

            insights.append(
                {
                    "type": "business_scale",
                    "title_key": "totalBusinessRevenueTitle",
                    "message_key": "totalBusinessRevenueMessage",
                    "params": {
                        "revenue": f"{total_revenue:,.2f}",
                    },
                }
            )

    # Average Order Value
    if revenue_column in df.columns:
        if dataset_id == "olist":
            order_count = (
                df["order_id"].nunique()
                if "order_id" in df.columns
                else 0
            )
        else:
            order_count = (
                pd.to_numeric(
                    df["orders"],
                    errors="coerce",
                ).sum()
                if "orders" in df.columns
                else 0
            )

        revenue_values = pd.to_numeric(
            df[revenue_column],
            errors="coerce",
        ).dropna()

        if order_count > 0 and not revenue_values.empty:
            total_revenue = float(revenue_values.sum())

            average_order_value = total_revenue / order_count

            insights.append(
                {
                    "type": "average_order_value",
                    "title_key": "averageOrderValueTitle",
                    "message_key": "averageOrderValueMessage",
                    "params": {
                        "value": f"{average_order_value:,.2f}",
                    },
                }
            )

    # Most Used Payment Method
    if dataset_id == "olist":
        payments = await get_payments(
            dataset_id,
            user_id,
        )

        if "payment_type" in payments.columns and not payments.empty:
            payment_counts = payments["payment_type"].dropna().value_counts()

            if not payment_counts.empty:
                top_payment_method = payment_counts.index[0]

                payment_name = PAYMENT_TRANSLATIONS.get(
                    top_payment_method,
                    str(top_payment_method).replace("_", " ").title(),
                )

                insights.append(
                    {
                        "type": "payment",
                        "title_key": "mostUsedPaymentMethodTitle",
                        "message_key": "mostUsedPaymentMethodMessage",
                        "params": {
                            "paymentMethod": payment_name,
                        },
                    }
                )

    elif "payment_method" in df.columns:
        payment_counts = df["payment_method"].dropna().value_counts()

        if not payment_counts.empty:
            top_payment_method = payment_counts.index[0]

            payment_name = (
                str(top_payment_method)
                .replace(
                    "_",
                    " ",
                )
                .title()
            )

            insights.append(
                {
                    "type": "payment",
                    "title_key": "mostUsedPaymentMethodTitle",
                    "message_key": "mostUsedPaymentMethodMessage",
                    "params": {
                        "paymentMethod": payment_name,
                    },
                }
            )

    # Business Opportunity
    if category_column in df.columns and revenue_column in df.columns:
        opportunity_df = df.copy()

        opportunity_df[revenue_column] = pd.to_numeric(
            opportunity_df[revenue_column],
            errors="coerce",
        )

        opportunity_df = opportunity_df.dropna(
            subset=[
                category_column,
                revenue_column,
            ]
        )

        if not opportunity_df.empty:
            category_revenue = (
                opportunity_df.groupby(category_column)[revenue_column]
                .sum()
                .sort_values(ascending=False)
            )

            total_revenue = float(
                opportunity_df[revenue_column].sum()
            )

            if not category_revenue.empty and total_revenue > 0:
                top_category = category_revenue.index[0]
                top_category_revenue = float(
                    category_revenue.iloc[0]
                )

                display_category = CATEGORY_TRANSLATIONS.get(
                    top_category,
                    str(top_category).replace("_", " ").title(),
                )

                revenue_share = (
                    top_category_revenue / total_revenue
                ) * 100

                if revenue_share >= 30:
                    insights.append(
                        {
                            "type": "opportunity",
                            "title_key": "growthOpportunityTitle",
                            "message_key": "growthOpportunityMessage",
                            "params": {
                                "category": display_category,
                                "percentage": f"{revenue_share:.1f}",
                            },
                        }
                    )

                if revenue_share >= 50:
                    insights.append(
                        {
                            "type": "alert",
                            "title_key": "businessAlertTitle",
                            "message_key": "businessAlertMessage",
                            "params": {
                                "category": display_category,
                                "percentage": f"{revenue_share:.1f}",
                            },
                        }
                    )

    # Overall Business Interpretation
    interpretation_parts = []

    if category_column in df.columns and revenue_column in df.columns:
        interpretation_df = df.copy()

        interpretation_df[revenue_column] = pd.to_numeric(
            interpretation_df[revenue_column],
            errors="coerce",
        )

        interpretation_df = interpretation_df.dropna(
            subset=[
                category_column,
                revenue_column,
            ]
        )

        if not interpretation_df.empty:
            category_revenue = (
                interpretation_df.groupby(category_column)[revenue_column]
                .sum()
                .sort_values(ascending=False)
            )

            total_revenue = float(
                interpretation_df[revenue_column].sum()
            )

            if not category_revenue.empty and total_revenue > 0:
                top_category = category_revenue.index[0]

                if dataset_id == "olist":
                    top_category = CATEGORY_TRANSLATIONS.get(
                        top_category,
                        str(top_category).replace("_", " ").title(),
                    )

                top_category_revenue = float(
                    category_revenue.iloc[0]
                )

                revenue_share = (
                    top_category_revenue / total_revenue
                ) * 100

                interpretation_parts.append(
                    {
                        "message_key": "interpretationTopCategory",
                        "params": {
                            "category": top_category,
                            "percentage": f"{revenue_share:.1f}",
                        },
                    }
                )

    if revenue_column in df.columns:
        revenue_values = pd.to_numeric(
            df[revenue_column],
            errors="coerce",
        ).dropna()

        if len(revenue_values) >= 2:
            first_revenue = float(revenue_values.iloc[0])
            last_revenue = float(revenue_values.iloc[-1])

            if first_revenue != 0:
                change_percent = (
                    (last_revenue - first_revenue)
                    / abs(first_revenue)
                ) * 100

                if change_percent > 0:
                    interpretation_parts.append(
                        {
                            "message_key": "interpretationRevenueIncreased",
                            "params": {
                                "percentage": f"{change_percent:.1f}",
                            },
                        }
                    )
                elif change_percent < 0:
                    interpretation_parts.append(
                        {
                            "message_key": "interpretationRevenueDeclined",
                            "params": {
                                "percentage": f"{abs(change_percent):.1f}",
                            },
                        }
                    )
                else:
                    interpretation_parts.append(
                        {
                            "message_key": "interpretationRevenueStable",
                        }
                    )

    if "review_score" in df.columns:
        review_scores = pd.to_numeric(
            df["review_score"],
            errors="coerce",
        ).dropna()

        if not review_scores.empty:
            average_review = float(review_scores.mean())

            if average_review >= 4:
                interpretation_parts.append(
                    {
                        "message_key": "interpretationSatisfactionStrong",
                    }
                )
            elif average_review >= 3:
                interpretation_parts.append(
                    {
                        "message_key": "interpretationSatisfactionModerate",
                    }
                )
            else:
                interpretation_parts.append(
                    {
                        "message_key": "interpretationSatisfactionAttention",
                    }
                )

    if interpretation_parts:
        insights.append(
            {
                "type": "interpretation",
                "title_key": "overallBusinessInterpretationTitle",
                "message_key": "overallBusinessInterpretationMessage",
                "message_parts": interpretation_parts,
            }
        )

    return {
        "dataset_id": dataset_id,
        "insights": insights,
    }