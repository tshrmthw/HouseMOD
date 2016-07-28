package com.markurz.wheresethan;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.ArrayList;

/**
 * Created by markkurtz on 4/6/16.
 */
public class DataPointsRecyclerAdapter extends RecyclerView.Adapter<DataPointViewHolder> {
    private ArrayList<DataPointCard> mDataPointCards;

    public DataPointsRecyclerAdapter() {
        mDataPointCards = new ArrayList<>();
    }

    @Override
    public DataPointViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View cardView = LayoutInflater.from(parent.getContext()).inflate(R.layout.card_data_point, parent, false);

        return new DataPointViewHolder(cardView);
    }

    @Override
    public void onBindViewHolder(DataPointViewHolder holder, int position) {
        mDataPointCards.get(position).bindViewHolder(holder);
    }

    @Override
    public int getItemCount() {
        return mDataPointCards.size();
    }

    @Override
    public int getItemViewType(int position) {
        return 0;
    }

    public ArrayList<DataPointCard> getDataPointCards() {
        return mDataPointCards;
    }
}
