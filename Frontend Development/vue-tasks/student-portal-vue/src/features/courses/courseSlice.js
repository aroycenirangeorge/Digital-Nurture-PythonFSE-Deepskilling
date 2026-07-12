import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getAllCourses } from '../../api/courseApi'; 

export const fetchAllCourses = createAsyncThunk(
  'courses/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const data = await getAllCourses();
      return data;
    } catch (error) {
      return rejectWithValue(error.message || 'Failed to fetch courses');
    }
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const courseSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllCourses.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAllCourses.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchAllCourses.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Something went wrong while loading courses.';
      });
  },
});

export const { clearError } = courseSlice.actions;

export const selectCourses = (state) => state.courses.items;
export const selectCoursesLoading = (state) => state.courses.loading;
export const selectCoursesError = (state) => state.courses.error;

export default courseSlice.reducer;